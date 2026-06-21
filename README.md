# project-template

新项目脚手架。已内置 `structure-guide` skill——任何结构性变更前 Claude 会自动加载它，避免目录瞎写、CLAUDE.md 膨胀等问题。

## 开始新项目

```bash
cp -r project-template /path/to/new-project
cd /path/to/new-project
claude
```

### 首次开第一次会话，交代这几件事

- **往 CLAUDE.md 顶部补**：项目定位、禁止事项、工作风格（可让 Claude 触发 structure-guide 的 `guides/claude-md.md` 看模板）。
- **要推送 GitHub 时**：把仓库名告诉 AI（或直接 `/git-push <仓库名>`）。账号默认 `zaizaixiaodi`，PAT 在 Wolai 笔记里取——AI 会按 `git-push` skill 现问现配，不用预填。

## 多轮开发（跨 session 接力）

需要多次会话才能完成的任务，靠 `PLAN.md`（任务协议）+ `HANDOFF.md`（接力文档）两层分工：

- **复杂任务开工**：按 `plan` skill 建 `PLAN.md`——目标、不做什么、验收标准、验证手段，防止"看起来做完了"。创建靠问不靠猜：你可主动 `/plan`；AI 觉得需求复杂会先问你要不要建；会话收尾没做完的任务会提示补建。
- **会话开始**：先读根目录 `HANDOFF.md` 接上进度（有 `PLAN.md` 则一并读）。
- **维护**：由 `handoff` skill 定纪律——当下态覆盖、沉淀物按性质流出、≤80 行不膨胀（它是接力存档点，不是流水账）。计划的方向性变更在"在途决策"记一行原因，不设 devlog（细节变更靠 git 历史兜底）。
- **一轮收尾**：`/done` 一步搞定（PLAN.md 完成则归档到 `archive/plans/` + 更新 HANDOFF.md + 提交推送）。
- 首次推送 GitHub 用 `git-push` skill。

## 测试/开发 structure-guide

- **日常修改**：直接在 `project-template/.claude/skills/structure-guide/` 下编辑
- **干净测试**：把整个 `project-template/` 复制到 metadevskill 外（如桌面），再进去启动 Claude，避免父目录的 init-project-context skill 干扰
