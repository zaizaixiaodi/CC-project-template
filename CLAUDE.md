## 结构变更前必读

> 此节为永久约束，无论项目如何演进都不得删除或修改。

创建/修改 CLAUDE.md、skill、subagent、rule、hooks 时，
先读 `.claude/skills/structure-guide/SKILL.md`，按其中的路由跳到对应 guide。

## 多轮开发

跨 session 的任务：会话开始先读 `PROGRESS.md` 接上进度，结束前按 `session-handoff` skill 更新（当下态覆盖、稳定决策迁出）。一轮收尾用 `done` skill（更新进度 + 提交推送）。
