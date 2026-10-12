# 权限与 hooks

权限与运行配置首先查当前 Codex 版本；项目配置使用 `.codex/config.toml`，不能照搬旧工具的 `settings.json` 和 `Bash(...)` 权限字符串。

沙箱限制文件和网络访问，审批策略控制何时请求执行授权。项目指令用于指导行为，不替代这两项控制。遵循已生效的用户或管理员配置，模板不要默认放宽权限。

当前官方配置支持生命周期 hooks，既可用配置中的 `hooks.<Event>`，也有 hooks 文件机制。具体事件、matcher、输入输出协议、Windows 命令覆盖与加载位置，先读 [官方 Hooks](https://learn.chatgpt.com/docs/hooks)。不要仅因事件同名就复制其他工具的 handler。

实现时把实际逻辑放可测试脚本：

1. 确认目标环境支持相应事件和配置字段。
2. 用最小输入运行脚本，检查退出码、输出和失败处理。
3. 在隔离工作区触发真实事件，观察结果，验证重复执行行为。

某个版本没有所需事件时，将自动化写成用户可执行的脚本或 skill，并说明需要手动执行；不要伪造已生效的 hook。

更多字段见 [官方配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)。
