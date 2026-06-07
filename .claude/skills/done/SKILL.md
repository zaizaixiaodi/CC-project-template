---
name: done
description: 一轮工作的手动收尾，组合 session-handoff（更新 PROGRESS.md）与 git 提交推送两步。适用于：完成一轮（或一个 session）开发后，手动归档进度并推送。不适用于：开发中途、单步小改动、或仅想更新进度不推送的场景。
disable-model-invocation: true
argument-hint: <提交信息，可选；缺省则据本轮改动自拟>
---

# done

一轮工作收尾：先固化进度，再推送。两步都引用现有 skill，不重复其细节。

## 第一步：更新 PROGRESS.md

按 `session-handoff` 的"会话结束"纪律更新根目录 `PROGRESS.md`：

- **当前 (Now)** 覆盖重写：写清本轮成果 + 下个 session 第一个具体动作。
- 勾掉完成的计划项；稳定的决策迁出到 `CLAUDE.md`/`rules` 并从 PROGRESS.md 删除。
- 守住 ≤80 行、禁流水账。

## 第二步：提交并推送

1. 自拟或采用 `$ARGUMENTS` 作为提交信息（一句话概括本轮改动，含 PROGRESS.md 更新）。
2. 已配置 remote 的仓库——常规推送：
   ```
   git add .
   git commit -m "<提交信息>"
   git -c http.proxy="" -c https.proxy="" push origin main
   ```
3. 尚未初始化或未设 remote → 转走 `git-push` 完整流程。

## 注意事项

- 本机代理 `127.0.0.1:17890`，推送必须用 `-c http.proxy="" -c https.proxy=""` 绕过（见 git-push）。
- 收尾性操作，**仅手动触发**，不自动运行。
- 推送前确认 `git status` 无意外文件入库。
