# Alembic 迁移"表已存在"错误完整解决方案

## 一、问题现象

执行 `alembic upgrade head` 时报错：

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1050, "Table 'sys_dept' already exists")
```

Alembic 尝试创建一张表，但数据库中该表已经存在，导致迁移中止。

---

## 二、根本原因

**核心问题：Alembic 迁移状态与数据库实际状态不一致。**

Alembic 通过数据库中的 `alembic_version` 表来追踪"当前执行到了哪个迁移版本"。如果一张表已经存在于数据库中，但 `alembic_version` 里没有记录对应的版本号，Alembic 就会认为这个迁移还没执行过，于是尝试重新建表——而表已经在了，自然报错。

### 典型触发场景

| 场景 | 说明 |
|------|------|
| **手动建表** | 直接跑 SQL 或用 `create_all()` 初始化了数据库，但没走 Alembic 流程 |
| **团队协作** | 有人手动在数据库建了表，但没有同步更新 `alembic_version` |
| **分支合并** | 多个分支各自产生了迁移脚本，合并后出现多个迁移链（两个 `<base>`），版本记录混乱 |
| **数据库恢复** | 从备份恢复数据库后，表结构是完整的，但 `alembic_version` 记录丢失或不完整 |

---

## 三、解决方案

### 方案一：`alembic stamp` 标记版本（推荐）

**原理**：`stamp` 只更新 `alembic_version` 表的版本号，不执行任何建表 SQL。相当于跳过施工，直接在"施工日志"上盖章。

```bash
# 标记单个迁移版本为已完成
uv run alembic stamp 577e5326c297
```

这在数据库中执行的操作等同于：

```sql
-- 如果 alembic_version 表已有记录
UPDATE alembic_version SET version_num = '577e5326c297';

-- 如果 alembic_version 表为空
INSERT INTO alembic_version (version_num) VALUES ('577e5326c297');
```

**适用场景**：确认数据库中的表结构已经完整且正确，只是 Alembic 不知道。

#### 单表报错 → 单次 stamp

如果只有一个迁移版本报错：

```bash
# 1. 查看报错信息中的版本号（如 577e5326c297）
# 2. stamp 该版本
uv run alembic stamp 577e5326c297
# 3. 继续升级
uv run alembic upgrade head
```

#### 连续多表报错 → stamp head 一步到位

如果表都是提前建好的，会一个接一个报"表已存在"。与其逐个 stamp，不如直接跳到最新版本：

```bash
# 直接将版本指针跳到最末尾
uv run alembic stamp head
# 验证当前版本
uv run alembic current
# 应该显示最新的 head 版本号，之后再 upgrade 不会有任何操作
uv run alembic upgrade head
```

**前提条件**：数据库中的表结构必须已经是完整且正确的。后续新增的迁移脚本（加新字段/新表）会正常执行，不受影响。

#### 多迁移链的情况

分支合并后可能出现两条独立的迁移链（两个 `<base>`），最终合并到一个 head。这种情况也只需：

```bash
uv run alembic stamp head
```

因为 `head` 指向最终的合并点，stamp 到 head 就覆盖了所有链。

---

### 方案二：修改迁移脚本，加入幂等保护

编辑报错的迁移脚本，在 `create_table` 前加判断：

```python
from alembic import op
from sqlalchemy import inspect

def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if 'sys_dept' not in inspector.get_table_names():
        op.create_table('sys_dept',
            # ... 原有列定义保持不变
        )
```

**优点**：具有幂等性，无论表是否存在都能正常执行，适合多环境部署。

**缺点**：需要修改每个迁移脚本，工作量大；且破坏了迁移脚本的不可变性原则（迁移脚本一旦提交就不应再修改）。

---

### 方案三：清库重来（仅限开发环境）

如果数据库中没有重要数据，可以从头开始：

```bash
# 回退到最初始状态（会删除所有表）
uv run alembic downgrade base
# 重新执行所有迁移
uv run alembic upgrade head
```

**警告**：`downgrade base` 会删除所有表和数据，仅用于无重要数据的开发环境。

---

## 四、完整排查流程

### 第一步：确认数据库实际状态

```sql
-- 查看报错的表是否存在
SHOW TABLES LIKE 'sys_dept';

-- 查看 Alembic 当前记录的版本号
SELECT * FROM alembic_version;
```

目的：搞清楚"表存在"但"Alembic 不知道"这个不一致是如何形成的。

### 第二步：确认表结构是否正确

```sql
DESCRIBE sys_dept;
SHOW CREATE TABLE sys_dept;
```

目的：对比迁移脚本中的建表 DDL，确认现有表结构是否完整。如果结构有差异（缺字段、类型不同），直接 stamp 可能导致后续迁移出问题，需要先补齐差异。

### 第三步：查看迁移历史，了解全貌

```bash
uv run alembic history
```

输出示例：

```
90b9b6b428b4, ee2414601e1c -> 20260429182000 (head) (mergepoint), add preference_payload
3f6b9d2c1a7e -> 90b9b6b428b4, merge_colleague_schema_changes
...
577e5326c297 -> 001_agno_sessions, add agno sessions table for AI module
<base> -> 577e5326c297, 迁移脚本
...
<base> -> 80ba0c08f64d, Create initial database structure from models
```

关键信息：
- 出现两个 `<base>` 说明有两条独立的迁移链（分支合并导致）
- `(head)` 标记的是最终合并后的最新版本
- `(mergepoint)` 标记的是合并点

### 第四步：执行 stamp 修复

表结构确认无误后：

```bash
# 一步到位，跳到最新版本
uv run alembic stamp head
```

### 第五步：验证修复结果

```bash
# 查看当前版本
uv run alembic current
# 应显示最新的 head 版本号

# 尝试升级，应该没有待执行的迁移
uv run alembic upgrade head
# 应显示 "Running upgrade ..." 为空或直接成功
```

### 第六步（预防）：统一团队迁移规范

1. **禁止手动建表**：所有结构变更必须通过 Alembic 迁移脚本管理
2. **CI/CD 检查**：加入 `alembic check`，提前发现迁移状态不一致
3. **合并分支前检查**：运行 `alembic heads`，如果有多个 head 需要先合并迁移分支：
   ```bash
   uv run alembic merge heads -m "merge migration branches"
   ```
4. **代码中使用 `create_all()` 的注意事项**：开发阶段可以用 `create_all()` 建表，但必须同时执行 `alembic stamp head` 同步版本号，否则生产环境部署时会冲突

---

## 五、`alembic stamp` 详解

### 它做了什么

`stamp` 只做一件事：更新 `alembic_version` 表中的版本号，**不执行任何迁移脚本中的 SQL**。

| 操作 | 执行建表 SQL | 更新版本号 |
|------|:----------:|:--------:|
| `alembic upgrade head` | 是 | 是 |
| `alembic stamp head` | **否** | 是 |

### 比喻理解

把 Alembic 想象成施工队，`alembic_version` 表就是施工日志。每完成一个阶段的施工，就在日志上盖章。`stamp` 的意思就是：跳过施工，直接盖章，告诉 Alembic "这个版本我已经做完了"。

### 常用命令

```bash
# 标记到最新版本（最常用）
uv run alembic stamp head

# 标记到指定版本
uv run alembic stamp 577e5326c297

# 查看当前版本
uv run alembic current

# 查看迁移历史
uv run alembic history

# 查看是否有多个 head
uv run alembic heads
```

---

## 六、决策流程图

```
alembic upgrade head 报 "Table already exists"
        │
        ▼
  表结构是否完整正确？
     ┌────┴────┐
     是        否
     │         │
     ▼         ▼
  stamp head  补齐差异字段后 stamp head
     │         │
     ▼         ▼
  alembic current 验证版本号
     │
     ▼
  alembic upgrade head → 成功
```

如果不确定表结构是否正确，可以对比迁移脚本中的 DDL 和实际表结构，或直接在测试环境用方案三（清库重来）验证。

---

## 七、常见问题

### Q: stamp 之后新增的迁移还能正常执行吗？

能。`stamp head` 只是把当前版本指针设到 head。之后你新增的迁移脚本版本号会大于当前 head，`upgrade head` 时会正常执行这些新迁移。

### Q: 多个 head 是什么意思？

多个 head 说明有两条或更多独立的迁移链（通常由分支合并导致）。需要先合并：

```bash
uv run alembic merge heads -m "merge migration branches"
```

这会生成一个合并迁移脚本，将多条链合并为一个 head。

### Q: 生产环境能用 stamp 吗？

可以，但要谨慎。必须先确认表结构与迁移脚本一致。建议在测试环境验证后再在生产环境执行。

### Q: 怎么避免这个问题再次发生？

核心原则：**数据库结构变更只通过 Alembic 管理，不要手动建表或改表**。如果开发时用了 `create_all()`，记得配套执行 `alembic stamp head`。
