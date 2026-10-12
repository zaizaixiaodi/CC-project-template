# 指令与命令规则

按目录生效的编码或写作约定放嵌套 `AGENTS.md`。按文件类型区分的约定可以在指令中明确条件并链接参考文档；Codex 不会自动把旧工具的 `rules/*.md` 和 `paths:` 当作条件指令加载。

Codex `.rules` 文件用于命令执行决策，采用 `prefix_rule()` 语法，不能写普通 Markdown：

```python
prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
    justification = "推送前需要检查目标与提交内容。",
)
```

使用当前运行环境支持的规则路径。规则与 shell 拆分、命令前缀有关，不等于文件访问沙箱。避免过宽的允许前缀。

创建规则后用 `codex execpolicy check` 验证命令，先查看该版本 `--help` 的参数。检查应包含匹配、不匹配和可能扩大的命令形式，并确认新会话实际加载规则。

来源：[官方 Rules 指南](https://learn.chatgpt.com/docs/agent-configuration/rules)。
