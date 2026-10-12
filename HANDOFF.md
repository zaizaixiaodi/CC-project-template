# HANDOFF

> 接力文档。会话开始先读本文件；结束前按 `handoff` skill 更新。≤80 行，禁流水账。

## 🎯 当前 (Now)
目标：保存 Codex 脚手架最新版，包含 MCP 与新增技能。
在途：Firecrawl OAuth、Context7 及两个新增技能已安装实测；用户要求推送到原 GitHub 仓库。
下一步：确认远端最新提交；新机器按 README 安装并自行完成 Firecrawl OAuth。

## 📋 计划 (Plan)
<!-- 存在 PLAN.md 时本段只留一行指针：见 PLAN.md（当前在第 N 步） -->
- [x] 迁移 6 个技能、结构指南和 AGENTS.md。
- [x] 新增 2 个 TOML 角色及验证用例。
- [x] Firecrawl / Context7 真实 MCP 调用通过。
- [x] find-skills / UI UX Pro Max 安装测试通过，内置 skill-creator 跳过。
- [ ] 完成本机策略阻挡的原生角色加载验收（见 tests/cli-results.md）。

## ⚖️ 在途决策 (Decisions)
<!-- 一条一行：选 X 弃 Y，因为 Z。稳定后迁 AGENTS.md/docs 并从此删除 -->
保留旧 Claude 文件用于追溯；Codex 只使用新入口和目录。
用户取消本轮 Claude 与 WorkBuddy 适配，仅配置 Codex。

## ⚠️ 踩坑 (Gotchas)
<!-- <现象> → <原因/绕法>。过时即删 -->
CLI 全局配置含不支持字段；测试使用 --ignore-user-config，未改全局配置。
CLI shell 被 host policy 拒绝；不以静态检查或手动角色委派替代原生加载验收。
