# Codex 扩展安装与验收（2026-10-12）

本轮按用户最新要求仅适配 Codex，未修改 Claude 或 WorkBuddy 的本机设置。

| 项目 | 安装状态 | 实际验收 |
|---|---|---|
| Firecrawl MCP | 已加入本机与项目配置，OAuth 登录成功 | Codex 实际调用 firecrawl_scrape，返回 HTTP 200，标题 Example Domain，命中缓存 |
| Context7 MCP | 已加入本机与项目配置 | resolve-library-id 找到 /vercel/next.js，query-docs 返回 App Router page/layout 文档 |
| find-skills | 项目源码与 Codex 用户技能已安装 | npx skills find 'ui ux' --owner nextlevelbuilder，退出码 0，找到 ui-ux-pro-max 等技能 |
| UI UX Pro Max | 项目源码与用户技能已安装，路径适配 Codex | 已安装路径运行设计系统、UX 查询、Next.js stack 查询均成功；3 项上游 stack 行为回归测试通过 |
| skill-creator | Codex 已内置，未重复安装 | 确认系统 SKILL.md 存在并读取，未复制系统技能 |
| 项目结构 | 8 skills、2 角色、MCP TOML 配置 | scripts/validate.py 通过，格式、引用和行数检查通过 |

用户技能目录为 `~/.agents/skills/`，仅安装 find-skills 与 ui-ux-pro-max。来源版本见 skills-sources.json，许可证保留在对应技能 LICENSE。
OAuth 凭据由 Codex 管理，不写入仓库；备用 API Key 未使用、未保存。

## MCP 实测过程

匿名 Firecrawl 能握手，但抓取返回 KEYLESS_ACCESS_NOT_AVAILABLE，失败记录见 mcp-firecrawl-results.json。改用用户提供的 OAuth 地址，codex mcp login firecrawl 返回 Successfully logged in。
随后使用正常用户配置启动 Codex，只读实际执行 firecrawl_scrape、resolve-library-id、query-docs 三次调用，均成功。结果见 firecrawl-auth-results.md 与 mcp-context7-results.json。
测试未上传本地材料、未执行 Git 写操作。忽略用户配置的前一次测试未发现 MCP，不作为通过证据。
用户原有的其他 MCP 存在 CLI 名称兼容警告，本轮未修改；新增两个服务器成功加载和调用。

之前子代理迁移的限制仍见 cli-results.md。本轮 MCP 通过不代表此前自定义子代理原生加载验收通过，记录分别保留。
