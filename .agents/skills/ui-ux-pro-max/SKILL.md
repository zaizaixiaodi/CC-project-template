---
name: ui-ux-pro-max
description: UI/UX design intelligence for web, mobile and desktop interfaces. Use for UI layout, visual design, accessibility, interaction, design systems and stack-specific interface implementation. Skip backend-only logic and non-visual infrastructure.
---
# UI/UX Pro Max for Codex

本技能来自 nextlevelbuilder/ui-ux-pro-max-skill，保留官方搜索脚本、数据与设计原则。

## 使用
1. 先读取 [完整工作流程](references/workflow.md)，按需读取 [优先级速查](references/quick-reference.md) 与 [交付检查](references/pro-rules.md)。
2. 根据任务选择最小搜索：新页面或整体视觉方向用 `--design-system`；单个问题用 `--domain`；已确定技术栈用 `--stack`。不预设技术栈。
3. 从本技能实际加载路径确定 `<skill-directory>`，用完整脚本路径运行，不依赖 Claude 插件变量或当前工作目录。

```powershell
python "<skill-directory>/scripts/search.py" "law firm dashboard accessible" --design-system -p "Law Dashboard"
python "<skill-directory>/scripts/search.py" "keyboard focus visible" --domain ux
python "<skill-directory>/scripts/search.py" "responsive dashboard layout" --stack nextjs
```

Python 3，无外部依赖；解释器不可用时查找 python3/py 或已配置的 Python 绝对路径。
需要落盘时显式使用 `--persist --output-dir "<用户授权的项目路径>"`；不要自动覆盖已有设计系统。
查询围绕一个主意图，检查命中内容是否适用于实际产品；结果不匹配时仅缩小查询重试一次，再说明限制。

数据是本地指导而非最新框架 API 的保证；涉及版本相关 API 时使用 Context7 验证实际版本。
