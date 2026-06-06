---
name: structure-guide
description: 项目结构与 Claude Code 配置文件的创建指南。当用户要创建或修改 CLAUDE.md、新建 skill（SKILL.md）、新建 subagent、新建 rule、配置 hooks/permissions 等结构性变更时使用。不适用于日常编辑代码或写业务内容。
disable-model-invocation: false
---

# 结构变更导航

用户要做的是**结构性变更**（改动 Claude Code 配置体系），不是写业务代码。

## 工作流程

1. **先读 `principles.md`** — 了解三层架构和所有变更都必须遵守的硬约束
2. **从下表选对应 guide 阅读全文**
3. **读完后再动手**，不要凭记忆操作

## 路由表

| 用户要做的事 | 阅读 |
|------------|-----|
| 写或改根目录 CLAUDE.md | `guides/claude-md.md` |
| 拆分或新建子目录 CLAUDE.md | `guides/subdirectory.md` |
| 新建 skill 或修改 SKILL.md | `guides/skill.md` |
| 新建 rule（含 paths 路径谓词） | `guides/rule.md` |
| 新建 subagent（独立上下文角色） | `guides/subagent.md` |
| 配置 hooks 或 permissions | `guides/hooks.md` |

## 跨类别的处理顺序

如果用户需求横跨多个类别，按下面顺序逐一处理（先骨架后细节）：

`CLAUDE.md` → `subdirectory` → `rule` → `skill` → `subagent` → `hooks`
