# project-template

新项目脚手架。已内置 `structure-guide` skill——任何结构性变更前 Claude 会自动加载它，避免目录瞎写、CLAUDE.md 膨胀等问题。

## 开始新项目

```bash
cp -r project-template /path/to/new-project
cd /path/to/new-project
claude
```

之后在 CLAUDE.md 顶部按需补充项目定位、禁止事项、工作风格等（可让 Claude 触发 structure-guide 的 `guides/claude-md.md` 看模板）。

## 多轮开发（跨 session 接力）

需要多次会话才能完成的任务，靠一份 `HANDOFF.md` 接力：

- **会话开始**：先读根目录 `HANDOFF.md` 接上进度。
- **维护**：由 `handoff` skill 定纪律——当下态覆盖、沉淀物按性质流出、≤80 行不膨胀（它是接力存档点，不是流水账）。
- **一轮收尾**：`/done` 一步搞定（更新 HANDOFF.md + 提交推送）。
- 首次推送 GitHub 用 `git-push` skill。

## 测试/开发 structure-guide

- **日常修改**：直接在 `project-template/.claude/skills/structure-guide/` 下编辑
- **干净测试**：把整个 `project-template/` 复制到 metadevskill 外（如桌面），再进去启动 Claude，避免父目录的 init-project-context skill 干扰
