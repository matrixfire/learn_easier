# Git: Save Work Mid-Development

## Problem
- 在開發功能到一半時，擔心程式碼遺失
- 不確定該用 `git stash` 還是 `git commit`

## Key Insight
- `git stash` = 暫時藏起來（抽屜）
- `git commit` = 正式存檔（保險箱）
- 兩者用途不同

## Recommendation
- **優先使用 `git commit`**
- 最安全、最常見的做法

## Why Commit is Better
- `stash` 容易忘記或搞混
- `commit` 有完整記錄和說明
- 不會遺失工作內容

## WIP Commit Pattern
```
git commit -m "WIP: 新增登入功能（未完成）"
```

## When to Use Stash
- 臨時切換到其他分支
- 不想 commit 半成品
- 記得用完取回來：
  ```
  git stash      # 藏起來
  git stash pop  # 取回來
  ```

## Summary
- 怕程式碼不見 → 用 `git commit -m "WIP: ..."`
- 臨時切換分支 → 用 `git stash`
