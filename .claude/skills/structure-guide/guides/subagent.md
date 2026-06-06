# 写 subagent 指南

## 何时用本指南

- 用户要做一个"独立上下文"的专精角色（如只读审查员、安全审计员）
- 用户要并行处理多个独立任务
- 用户要限制某个任务的工具权限（如"这个任务只能读不能写"）

## 何时不用

- 用户要的是"可手动调用的工作流" → 跳 `skill.md`（skill 共享主对话上下文，更轻量）
- 用户只是要一段提示词模板 → 跳 `skill.md`
- 用户要"全局事实约束" → 跳 `claude-md.md`

---

## 核心方法论

### subagent 是独立上下文实例

Subagent 拥有**独立的上下文窗口**，与主对话隔离。主 Claude 把任务委托给它，它的工作历史不会污染主对话；主对话的历史也不会干扰它。

### subagent vs skill

| 维度 | skill | subagent |
|------|-------|---------|
| 执行主体 | 主 Claude | 独立 Claude 实例 |
| 上下文 | 共享主对话 | 完全独立 |
| 用途 | 步骤化流程 | 专精角色、并行、隔离 |
| 工具权限 | 继承主对话 | 可单独限制（`tools:` 字段） |

### 触发方式

- 用户输入 `@<agent-name>` 主动委托
- 主 Claude 根据 `description` 自动委托

### 持久 memory

subagent 可以有专属 memory（`memory: project` / `local` / `user`），与主对话 auto memory 隔离。

---

## 决策规则

| 情况 | 方案 |
|-----|------|
| 任务必须"只读" | `tools: Read, Grep, Glob`（不含 Edit/Write） |
| 任务并行处理 | 多个 subagent 同时跑 |
| 需要专属记忆 | 加 `memory: project`（或 local/user） |
| 简单任务、不需要独立上下文 | 用 skill 替代，更轻量 |
| 高风险委托（如自动 commit） | **不建议**给 subagent，主对话保留控制权 |

---

## 模板

`.claude/agents/<agent-name>.md`：

```markdown
---
name: <agent-name>
description: <做什么>。当用户/主 Claude 需要 <触发场景> 时委托给它。不适用于 <排除场景>。
tools: Read, Grep, Glob
---

你是 <角色定位>。你的职责：

1. <职责 1>
2. <职责 2>
3. <职责 3>

约束：
- <限制 1，如"不修改任何文件"或"每条意见必须注明位置">
- <限制 2>
```

### 带专属 memory 的版本

```markdown
---
name: <agent-name>
description: ...
tools: ...
memory: project
---

<系统提示>
```

---

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|--------|
| 给只读角色配 Edit/Write 工具 | 越权风险 | 严格按角色裁剪 `tools:` |
| description 不写"何时委托" | 主 Claude 不知道何时用 | 三要素齐全 |
| 把一个 skill 直接搬过来当 agent | 浪费独立上下文能力 | skill 和 agent 用途不同，按需选 |
| 让 subagent 处理高风险操作（推送、删除） | 失去主对话控制 | 高风险任务留主对话或手动触发 |
| 写在 `~/.claude/agents/` 但本意是项目专属 | 污染全局 | 默认 `.claude/agents/`，跨项目才放 `~/` |
| 没设置 memory 但需要跨次记忆 | 每次都从零开始 | 加 `memory: project` |

---

## 完成后自检

- [ ] 文件路径是 `.claude/agents/<name>.md`
- [ ] frontmatter 含 `name` + `description`（三要素齐全）
- [ ] 只读角色裁掉了 Edit/Write 等写工具
- [ ] 高风险操作没委托给 subagent
- [ ] 默认放项目级 `.claude/agents/`，不污染 `~/.claude/`
