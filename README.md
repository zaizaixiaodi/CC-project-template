# Codex 工作流脚手架

Claude 版迁移为 Codex 项目模板，保留计划、接力、按天日志三层状态。

## 使用

在 Codex 桌面端把本目录作为项目打开，新建项目内会话；或进入本目录运行 `codex`。按客户端提示信任项目，以加载项目配置。
本仓库保存项目级配置与技能源码；个人 OAuth 凭据由 Codex 单独保管，不随 Git 同步。
开新项目时复制工作文件，排除 `.git`、`tests/.tmp` 和历史开发日志，保留原模板。

| 路径 | 用途 |
|---|---|
| AGENTS.md | 项目约定和上下文路由 |
| .agents/skills/ | 六个技能，显式调用 `$skill-name` |
| .codex/agents/*.toml | workflow-reviewer 和 workflow-tester 子代理 |
| .codex/config.toml | 启用子代理，最多三个并发子代理 |
| PLAN.md | 任务目标与验收，完成后归档 |
| HANDOFF.md | 当前状态与下一步，覆盖更新 |
| devlog/YYYY-MM-DD.md | 按天追加的历史，按需读取 |

| 调用 | 功能 |
|---|---|
| `$plan 整理会议材料` | 创建或更新任务协议 |
| `$handoff` | 更新接力 |
| `$devlog 2026-10-12` | 查看指定日期，或按请求记录日志 |
| `$done` | 归档已验收计划、更新接力、追加日志 |
| `$git-push` | 按明确授权提交或推送 |
| `$structure-guide` | 导航 Codex 配置维护 |

done 和 git-push 仅显式调用。普通收尾不会自动提交或推送。
不固定账号、模型、代理或分支，不保存凭据；项目设置不改用户全局配置。

子代理请求示例：`请委派 workflow-reviewer 检查技能，再让 workflow-tester 在 tests/.tmp 验证接力流程。`
子代理继承运行环境和权限；主代理负责汇总验收。

## 验证

Python 3.11+ 与 PyYAML：`python scripts/validate.py`。
行为用例见 [tests/behavioral-cases.md](tests/behavioral-cases.md)，实际行为结果见 [tests/behavior-results.md](tests/behavior-results.md)。
结构校验、手动读取角色后的委派、客户端原生发现分别验收，不能互相替代。

`.claude/`、CLAUDE.md 和旧参考文章保留作为历史；当前版本只适配 Codex，使用 AGENTS.md 与新目录。

## MCP 与新增技能

项目 `.codex/config.toml` 已配置 Firecrawl OAuth 与 Context7。已有项目配置时先合并两个 mcp_servers 表，不覆盖其他配置。
本机跨项目安装：

```powershell
codex mcp add firecrawl --url https://mcp.firecrawl.dev/v2/mcp-oauth
codex mcp login firecrawl
codex mcp add context7 --url https://mcp.context7.com/mcp
python scripts/install_codex_skills.py
```

Firecrawl 登录需要用户在浏览器授权；本机已完成 OAuth，并实际验证抓取成功。免 Key 接口在本次测试中拒绝匿名抓取，不能作为已验证替代方案。新机器仍需自行登录。
Context7 已实际通过库检索与文档查询。可用 `$find-skills` 搜索技能，`$ui-ux-pro-max` 获取 UI/UX 设计建议；`$skill-creator` 为 Codex 内置，无需重复安装。
新增用户技能在下一轮对话可发现；看不到时重新打开项目会话。

UI UX Pro Max 的脚本、数据、许可证来自官方仓库，入口已去除 Claude 插件路径依赖。完整原工作流迁入 references/workflow.md，脚本按技能实际路径调用。
安装脚本不会覆盖已有不同版本；需要升级时先比较本地内容。

## 方案对齐与实现技能

| 调用 | 使用时机 |
|---|---|
| `$think` | tw93 的方案判断与头脑风暴，先对齐方向和可验证计划 |
| `$grill-me` | 连续追问，把目标、边界与取舍问清楚，不写项目文档 |
| `$grill-with-docs` | 带项目资料的追问，已确认术语沉淀到 CONTEXT.md，关键取舍形成 ADR |
| `$implement` | 实现已确认计划或 Issue，按公开接口测试并审查；提交需授权 |
| `$ponytail` | 清理过度设计，保留任务要求、边界验证与错误处理 |

典型顺序：`$think` 判断方向 → `$grill-with-docs` 澄清并记录 → `$implement` 执行 → `$ponytail` 检查多余复杂度。可按实际需求跳过已完成的阶段。
grill-me、grill-with-docs、implement 保留上游的仅显式调用策略；不会自动触发访谈或实现。

必要依赖已一并安装：grilling、domain-modeling、tdd、code-review、codebase-design。它们通过实际文件链接加载，不依赖 Claude 的 Skill tool。
本模板默认用 CONTEXT.md 存词汇；已有 GLOSSARY.md 的项目沿用原文件，避免两份词汇库。CONTEXT.md 不承担计划或日志职责，PLAN/HANDOFF 分工保留。
ADR 仅用于难以反悔、缺乏背景难理解、且存在真实取舍的决策；未确认选择不写成定论。

新一批行为验收见 [tests/planning-skills-results.md](tests/planning-skills-results.md)，来源提交与适配说明见 skills-sources.json。

验证记录见 [tests/integration-results.md](tests/integration-results.md)。MCP 直接测试：`python scripts/test_mcp.py context7 --live`；该脚本不读取 Codex OAuth 凭据，不能验证 OAuth 抓取。

官方依据：[Skills](https://learn.chatgpt.com/docs/build-skills)、[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)。
