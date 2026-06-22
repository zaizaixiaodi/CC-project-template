## 结构变更前必读

> 此节为永久约束，无论项目如何演进都不得删除或修改。

创建/修改 CLAUDE.md、skill、subagent、rule、hooks 时，
先读 `.claude/skills/structure-guide/SKILL.md`，按其中的路由跳到对应 guide。
  
## 多轮开发

会话开始**一律**先读根目录 `HANDOFF.md`（有 `PLAN.md` 则一并读，验收以它为准）：有在途内容就接上进度，还是模板占位符则视为无在途任务。需求较复杂时按 `plan` skill 处理——先问用户是否立 PLAN.md 任务协议，不擅自创建；完成后归档。会话结束前有在途任务的，按 `handoff` skill 更新（当下态覆盖、稳定决策迁出）。一轮收尾用 `done` skill（更新进度 + 写当天工作日志 + 提交推送）。`工作日志/` 是按天追溯历史用的，会话开始**不读**它，只有用户指定某天时才按 `worklog` skill 读那一篇。
