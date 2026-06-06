# project-template

新项目脚手架。已内置 `structure-guide` skill——任何结构性变更前 Claude 会自动加载它，避免目录瞎写、CLAUDE.md 膨胀等问题。

## 开始新项目

```bash
cp -r project-template /path/to/new-project
cd /path/to/new-project
claude
```

之后在 CLAUDE.md 顶部按需补充项目定位、禁止事项、工作风格等（可让 Claude 触发 structure-guide 的 `guides/claude-md.md` 看模板）。

## 测试/开发 structure-guide

- **日常修改**：直接在 `project-template/.claude/skills/structure-guide/` 下编辑
- **干净测试**：把整个 `project-template/` 复制到 metadevskill 外（如桌面），再进去启动 Claude，避免父目录的 init-project-context skill 干扰
