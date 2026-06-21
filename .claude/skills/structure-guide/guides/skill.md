# 写 skill 指南

> 硬约束（文件夹结构、≤200 行、description 三要素、禁 `commands/`、禁写 `~/.claude/`）已在 `principles.md` 讲过，本文件只补 skill 专属的写法。

## 何时用本指南

- 用户要新建一个可用 `/xxx` 调用的 skill
- 用户要修改现有 `SKILL.md`
- 用户要把一段多步骤流程从 CLAUDE.md 抽出来变成 skill

## 何时不用

- 用户只是问"skill 是什么" → 直接讲概念，不要建文件
- 流程少于 3 步且只用一次 → 写在对话里即可
- 用户要建独立上下文的角色 → 跳 `subagent.md`
- 用户要写"每次会话都生效的事实约束" → 跳 `claude-md.md` 或 `rule.md`

---

## description 三要素（最关键字段）

`description` 决定 Claude 能否自动识别并调用这个 skill。**必须包含三件事**：做什么、何时用、何时不用。

错误示例（太模糊，Claude 不知道何时该用）：
```yaml
description: 审查合同
```

正确示例：
```yaml
description: 对用户提供的合同草稿进行法律风险审查，输出风险评级和修改建议。适用于签署前审查。不适用于已发生争议的合同的事后分析。
```

## Progressive Disclosure（渐进式披露）

SKILL.md 是入口，保持精简。详细规则、参考、模板拆到附件文件，SKILL.md **引用**而不是**复制**：

```markdown
## 详细规则
完整字段表见 [reference.md](reference.md)
```

附件可选结构：
```
.claude/skills/<skill-name>/
├── SKILL.md           ← 主入口，必需
├── reference.md       ← 可选：详细说明，按需加载
└── templates/         ← 可选：模板和示例
```

---

## 字段决策规则

| 情况 | 方案 |
|-----|------|
| 高风险操作（删除、推送、提交、群发） | `disable-model-invocation: true`，禁止 Claude 自动触发 |
| 内部协作流程，不希望出现在 `/` 菜单 | `user-invocable: false` |
| 接受参数 | 加 `argument-hint: <参数说明>`，正文用 `$ARGUMENTS` 或 `$1` 引用 |
| 涉及大量参考材料 | 拆到附件，SKILL.md 只引用 |

---

## 模板

新建文件 `.claude/skills/<skill-name>/SKILL.md`：

```markdown
---
name: <skill-name>
description: <做什么>。适用于：<触发场景>。不适用于：<排除场景>。
disable-model-invocation: false
argument-hint: <参数说明（无参数则删除此行）>
---

# <skill 名称>

## 流程

1. <第一步>
2. <第二步>
3. <第三步>

## 输出格式

- <格式要求 1>
- <格式要求 2>
```

---

## skill 专属的易错点

| 错误 | 后果 | 正确做法 |
|------|------|--------|
| description 只写"做 XX" 不写何时用/不用 | 自动触发率低或误触发 | 三要素齐全 |
| 高风险操作没设 `disable-model-invocation` | 被 Claude 自动触发，误删/误推 | 设 `true` |
| 路由式 skill 内部又触发自己 | 死循环风险 | 用引用文档（读 md），不重新触发 skill |

## 完成后自检

- [ ] frontmatter 的 `description` 三要素齐全
- [ ] 高风险操作设了 `disable-model-invocation: true`
- [ ] 接受参数的写了 `argument-hint`，正文用 `$ARGUMENTS`/`$1`
- [ ] 结构/行数等通用硬约束已对照 `principles.md`
