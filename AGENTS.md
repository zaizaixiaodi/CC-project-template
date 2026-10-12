# Codex 工作流脚手架

本项目提供项目级 skills、subagents 和跨会话状态文档。默认用中文沟通。

## 上下文
- 会话开始读取根目录 HANDOFF.md；模板占位符表示没有在途任务。
- 存在 PLAN.md 时一并读取，以其验收标准为准。
- 不自动读取 devlog/；用户追溯某天时只读取对应日期。
- 结构变更前读取 `.agents/skills/structure-guide/SKILL.md`，按路由阅读相关指南。
- Skills 位于 `.agents/skills/`，显式调用用 `$skill-name`，不使用 Claude slash commands。

## 工作纪律
- 已授权任务直接完成；复杂任务可维护 PLAN.md，不把创建计划变成重复审批。
- 根 AGENTS.md ≤200 行，HANDOFF.md ≤80 行，PLAN.md ≤100 行；这是本模板维护约定，不是 Codex 平台限制。
- 稳定规范放 AGENTS.md，描述性知识放 docs/；工作流程放 skills。
- 不修改用户全局设置；不在仓库保存凭据。
- 用户明确要求本机安装时可修改对应用户级设置，合并新增项目并保留已有配置；OAuth 凭据不复制到项目。
- `$done` 更新状态和日志；只有用户明确要求提交或推送时执行 Git 写操作。
- 不自动覆盖远端、强推或用 ours 丢弃冲突。

## 子代理与验证
- 用户要求委派或测试时使用 `.codex/agents/` 中的专用角色。
- 独立任务可并行；写任务必须限定文件所有权，主代理负责汇总和验收。
- `workflow-reviewer` 只读审查，`workflow-tester` 在指定临时目录进行行为验证。
- 若委派工具支持自定义角色选择，使用对应 TOML 角色；否则主代理先读取角色指令，再在委派消息中传入，并明确这是手动加载。只读限制同时受父级权限约束，不能声称 TOML 的 sandbox 设置已应用。
- 结构检查：`python scripts/validate.py`（Python 3.11+，需 PyYAML）。
- 行为用例见 `tests/behavioral-cases.md`；结构检查不等于模型调用成功。

## MCP 与扩展技能
- 需要读取已知网页时使用 Firecrawl；未登录时报告状态，不假定可抓取。
- 库和框架 API 的版本相关问题使用 Context7：先 resolve-library-id，再 query-docs，核对实际版本。
- 查找可安装技能用 find-skills；UI/UX 请求用 ui-ux-pro-max；创建技能用 Codex 内置 skill-creator。
- MCP 安装与实测记录见 tests/integration-results.md。
- 方案判断用 think；显式访谈用 grill-me / grill-with-docs，后者按已确认术语和决策更新 CONTEXT.md 与 ADR。
- 已确认计划用 implement；清理过度设计用 ponytail。既有授权和已确认测试接口无需重复确认。
- 支持技能通过相邻 SKILL.md 链接读取；依赖图见 skills-dependencies.json，新增行为验收见 tests/planning-skills-results.md。
