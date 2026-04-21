# Git 基础知识

## 概述

Git是一个**版本控制系统**，主要功能包括：
- **跟踪代码变更**: 记录每次修改历史
- **多人协作同步**: 不同开发者之间的代码同步
- **分支管理**: 测试更改而不丢失原始代码
- **版本回退**: 恢复到旧版本

---

## Git 三大作用

### 1. 版本控制
```
创建文件 → 添加行 → 删除行 → 回退
```
每次更改都会被记录，可以随时查看历史版本。

### 2. 协作同步
```
开发者A → GitHub ← 开发者B
```
多人同时修改同一文件，Git帮助合并更改。

### 3. 分支开发
```
主分支 (master) → 功能分支 (feature) → 合并
```
在不同分支独立开发，互不影响。

---

## 基本命令

### 1. git clone
**作用**: 从远程仓库克隆代码到本地

```bash
git clone <url>
```

**示例**:
```bash
git clone https://github.com/user/repo.git
```

---

### 2. git add
**作用**: 将文件更改添加到暂存区

```bash
git add <filename>
```

**示例**:
```bash
git add foo.py
# 输出: Changes to be committed: modified: foo.py
```

---

### 3. git commit
**作用**: 将暂存区的更改提交到本地仓库

```bash
git commit -m "message"
```

**示例**:
```bash
git commit -m "Add line"
```

**说明**: 提交信息应该清晰描述更改内容

---

### 4. git status
**作用**: 查看当前仓库状态

```bash
git status
```

**输出示例**:
```
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)
```

---

### 5. git push
**作用**: 将本地提交推送到远程仓库

```bash
git push
```

**说明**: 将本地分支的更改上传到GitHub

---

### 6. git pull
**作用**: 从远程仓库拉取并合并到本地

```bash
git pull
```

**说明**: 等同于 `git fetch` + `git merge`

---

## 分支管理

### git branch
**作用**: 查看或创建分支

```bash
# 查看所有分支
git branch

# 创建新分支
git branch <branch-name>

# 删除分支
git branch -d <branch-name>
```

---

### git checkout
**作用**: 切换分支或恢复文件

```bash
# 切换到指定分支
git checkout <branch-name>

# 创建并切换到新分支
git checkout -b <branch-name>

# 恢复文件到最后一次提交的状态
git checkout <filename>
```

---

### git merge
**作用**: 合并分支到当前分支

```bash
git merge <branch-name>
```

**说明**: 将指定分支的更改合并到当前分支

---

## 高级操作

### git log
**作用**: 查看提交历史

```bash
git log
```

**输出示例**:
```
commit 436f6d6d6974204d73672048657265
Author: Brian Yu <brian@cs.harvard.edu>
Date:   Tue Jan 14 14:06:28 2020 -0400
    Remove a line

commit 57656c636f6d6520746f20576562
Author: Brian Yu <brian@cs.harvard.edu>
Date:   Tue Jan 14 14:05:28 2020 -0400
    Add a line
```

---

### git reset
**作用**: 重置仓库状态

```bash
# 软重置（保留更改）
git reset HEAD

# 硬重置（放弃所有更改）
git reset --hard HEAD

# 重置到指定提交
git reset --hard <commit-hash>

# 重置到远程主分支状态
git reset --hard origin/master
```

**警告**: `--hard` 会永久删除未提交的更改

---

## 合并冲突

### 冲突产生
当同一文件的同一行被不同人修改时，`git pull`会产生冲突：

```
CONFLICT (content): Merge conflict in foo.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 冲突标记
```
a = 1
<<<<<<< HEAD
b = 2
=======
b = 0
>>>>>>> 57656c636f6d6520746f20576562
c = 3
d = 4
e = 5
```

| 标记 | 说明 |
|------|------|
| `<<<<<<< HEAD` | 你本地更改的开始 |
| `=======` | 分隔线 |
| `>>>>>>> <hash>` | 远程更改的结束 |

### 解决冲突步骤
1. 编辑文件，保留需要的代码
2. 删除冲突标记（`<<<<<<<`, `=======`, `>>>>>>>`）
3. `git add <filename>`
4. `git commit`

---

## 远程仓库

### git fetch
**作用**: 从远程获取最新更改，但不合并

```bash
git fetch
```

**说明**: 获取后需手动执行 `git merge origin/master`

---

### Fork 和 Pull Request

**Fork**: 复原他人的仓库到自己账户下

**Pull Request**: 请求原仓库拥有者合并你的更改

流程：
1. Fork目标仓库
2. 在自己的仓库中修改
3. 提交Pull Request
4. 原仓库审核者审查并合并

---

## HEAD 指针

**HEAD**: 指向当前所在的分支或提交

```
← master    ← feature    ← HEAD
```

当切换分支时，HEAD会移动到该分支的最新提交。

---

## 工作流程示例

### 基本流程
```bash
# 1. 克隆仓库
git clone <url>

# 2. 修改文件
# 编辑文件...

# 3. 查看状态
git status

# 4. 添加更改
git add <filename>

# 5. 提交更改
git commit -m "描述信息"

# 6. 推送到远程
git push

# 7. 拉取远程更改
git pull
```

### 分支开发流程
```bash
# 1. 创建并切换到新分支
git checkout -b feature-branch

# 2. 在分支上开发
# 修改文件...
git add .
git commit -m "添加新功能"

# 3. 切回主分支
git checkout master

# 4. 合并功能分支
git merge feature-branch

# 5. 删除已合并的分支
git branch -d feature-branch

# 6. 推送合并结果
git push
```

---

## 常见问题

### 问题1: 如何放弃本地更改？
```bash
git checkout .
# 或
git reset --hard HEAD
```

### 问题2: 如何查看远程仓库地址？
```bash
git remote -v
```

### 问题3: 如何修改最后一次提交信息？
```bash
git commit --amend -m "新的提交信息"
```

### 问题4: 如何查看文件修改内容？
```bash
git diff <filename>
```

### 问题5: 如何取消已暂存的更改？
```bash
git reset HEAD <filename>
```
