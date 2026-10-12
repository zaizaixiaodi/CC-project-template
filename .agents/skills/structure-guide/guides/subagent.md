# Codex subagent

用于职责清晰的独立任务。主代理给出任务、输入、修改范围和验收条件，子代理返回结果与证据。并行编辑时分配不重叠的文件。

项目角色放 `.codex/agents/<name>.toml`，不是带 YAML frontmatter 的 Markdown：

```toml
name = "reviewer"
description = "检查改动的正确性与回归风险，适用于已有实现的审查。"
sandbox_mode = "read-only"
developer_instructions = """
读取相关实现，指出可复现的问题并附文件位置。
只提出有证据的意见，不修改文件。
"""
```

启用和限制并发的项目配置：

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 3
```

必填字段为 `name`、`description`、`developer_instructions`。没有实际需求时继承模型；不要硬编码模型、旧工具的 `tools:` 或 `memory:` 字段。只读权限使用沙箱配置并在目标环境验证。

使用自然语言要求 Codex 委托给具体角色。验证需要实际派发任务并取得角色返回；文件解析成功不证明角色已被加载。

如果客户端委派接口没有自定义角色参数，先读取 TOML 中的 developer_instructions，再将职责与约束传入子代理消息。这是手动加载角色的兼容路径，应单独记录；不能据此声称 TOML 自动发现或其中的 sandbox_mode 已生效。父会话的权限约束仍适用。

来源：[官方子代理指南](https://learn.chatgpt.com/docs/agent-configuration/subagents)。
