---
name: structure-guide
description: 创建和修改 Codex 项目指令、技能、子代理及运行配置时提供结构导航。适用于 AGENTS.md、SKILL.md、custom agents、命令规则和 hooks 的变更，不适用于普通业务代码或内容编辑。
---

# 结构变更导航

先读 [通用原则](principles.md)，再按实际任务读取对应指南。读取文档即可，不要再次调用本 skill。

| 任务 | 指南 |
|---|---|
| 根项目指令 | [AGENTS.md](guides/agents-md.md) |
| 模块专属指令 | [子目录](guides/subdirectory.md) |
| 可复用流程 | [Skill](guides/skill.md) |
| 命令审批规则、按文件范围的约定 | [规则](guides/rule.md) |
| 独立角色与并行任务 | [Subagent](guides/subagent.md) |
| 权限、沙箱和生命周期自动化 | [配置](guides/hooks.md) |

跨类别变更先确定指令范围，再处理流程、角色和运行配置。完成后检查文件引用、配置解析以及实际加载行为；静态格式正确不等于运行可用。
