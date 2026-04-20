# Git & GitHub 速查笔记

---

## 一、Git 是什么

命令行版本控制工具，四大核心能力：
- **追踪变更** — 保存代码快照
- **多人协作** — push/pull 同步代码
- **分支开发** — 隔离新功能，不影响主线
- **回滚代码** — 恢复到任意历史版本

> **Repository（仓库）**：存放项目所有文件的地方，分 **Remote**（云端）和 **Local**（本地）两种。

---

## 二、GitHub

托管 Git 仓库的网站。

### 创建仓库
`+ → New repository` → 填写名称、描述、公开/私有、可选 README

### 克隆到本地
```bash
git clone <url>       # 下载远程仓库到本地
cd <repo-name>        # 进入目录
```

### 添加文件追踪
```bash
git add <file>        # 追踪指定文件
git add .             # 追踪全部文件
```

---

## 三、Commits（提交）

```bash
git commit -m "描述"          # 提交快照
git commit -amam "描述"         # add + commit 合并（仅限已追踪文件）
git status                    # 查看本地与远程的差异
git push                      # 推送到 GitHub
git pull                      # 拉取远程最新代码
git log                       # 查看提交历史（含 hash）
```

---

## 四、Merge Conflicts（合并冲突）

**触发时机**：push 或 pull 时，同一行被不同人修改。

**冲突格式**：
```
<<<<< HEAD
b = 2          ← 你的版本
=====
b = 3          ← 对方的版本
>>>>> [hash]
```
手动保留一个版本，删除标记符后重新 commit。

### 回滚命令
```bash
git reset --hard <commit-hash>   # 回到指定提交
git reset --hard origin/master   # 回到远程最新版本
```

---

## 五、Branching（分支）

**用途**：开发新功能时不污染主线，完成后再合并。

```
master: A → B → C
                 ↘ feature → D → E
                                  ↘ merge back
```

```bash
git branch                        # 查看当前分支（* 标注）
git checkout -b <new-branch>      # 创建并切换新分支
git checkout <branch>             # 切换分支
git merge <other-branch>          # 合并分支（先切回 master）
```

> **HEAD** 指向当前所在分支，默认为 `master`。

---

## 六、More GitHub Features（进阶功能）

| 功能 | 说明 |
|------|------|
| **Fork** | 复制他人仓库，自己拥有所有权，点击右上角 Fork 按钮 |
| **Pull Request** | 将你 fork 后的修改请求合并回原仓库；开源协作的核心流程 |
| **GitHub Pages** | 免费发布静态网站：建仓库 → 放 `index.html` → push → Settings → GitHub Pages → 选 master → 获得 URL |

---

**下一讲：Python 🐍**
