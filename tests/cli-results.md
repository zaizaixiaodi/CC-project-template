# Codex CLI 实测记录

日期：2026-10-12；CLI：0.162.0-alpha.17.2。

1. `codex exec --strict-config ...`：启动失败，全局 config.toml 含不支持的 `mcp_servers.<server>.type`。未改全局配置。
2. `codex exec --ignore-user-config --strict-config --ephemeral ...`：可启动；只读 shell 被 host policy 拒绝。子代理报 `no rollout found for thread id`，未启动成功。
3. 去掉 `--ephemeral`、在项目目录启动普通测试会话：成功创建 `fork_turns: none` 子代理 `/root/workflow_reviewer`。但主/子代理文件读取都被策略拒绝，未完成原生自定义角色加载验证。

第三次会话可发现四个允许隐式调用的项目 skills：devlog、handoff、plan、structure-guide。
done 与 git-push 设置 explicit-only；本次没有完成显式调用发现验证，不能由普通技能列表缺席认定它们失效。

结论：CLI 启动和普通子代理委派通过；原生 TOML 角色加载、全部六个 skill 的 CLI 调用未通过完整验收，受本机运行策略限制。手动加载角色的行为测试另见 behavior-results.md。
不会通过关闭沙箱或修改全局审批规则绕过上述限制。
