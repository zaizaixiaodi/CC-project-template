# 写 skill 指南

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

## 核心方法论

### skill 是文件夹，不是一个 .md 文件

正确结构：
```
.claude/skills/<skill-name>/
├── SKILL.md           ← 主入口，必需
├── reference.md       ← 可选：详细说明，按需加载
└── templates/         ← 可选：模板和示例
```

**典型错误**：直接在 `.claude/skills/` 下放 `git-push.md`——Claude Code 不会识别为 skill。正确做法是 `.claude/skills/git-push/SKILL.md`。

### Progressive Disclosure（渐进式披露）

SKILL.md 是入口，保持精简（≤ 200 行）。详细规则、参考、模板拆到附件文件，SKILL.md **引用**而不是**复制**：

```markdown
## 详细规则
完整字段表见 [reference.md](reference.md)
```

### description 三要素（最关键字段）

`description` 决定 Claude 能否自动识别并调用这个 skill。**必须包含三件事**：

1. **做什么**：功能一句话描述
2. **何时用**：触发场景，越具体越好
3. **何时不用**：明确排除场景，避免误触发

错误示例：
```yaml
description: 审查合同
```
太模糊，Claude 不知道何时该用。

正确示例：
```yaml
description: 对用户提供的合同草稿进行法律风险审查，输出风险评级和修改建议。适用于签署前审查。不适用于已发生争议的合同的事后分析。
```

---

## 决策规则

| 情况 | 方案 |
|-----|------|
| 流程简单、无附件 | 仍要 `<skill-name>/SKILL.md` 文件夹结构，不要省略 |
| 涉及大量参考材料 | 拆到附件，SKILL.md 只引用 |
| 高风险操作（删除、推送、提交、群发） | `disable-model-invocation: true`，禁止 Claude 自动触发 |
| 内部协作流程，不希望出现在 `/` 菜单 | `user-invocable: false` |
| 接受参数 | 加 `argument-hint: <参数说明>`，正文用 `$ARGUMENTS` 或 `$1` 引用 |
| 项目专属流程 | `.claude/skills/`（默认） |
| 跨所有项目都要用 | 用户明确同意后才放 `~/.claude/skills/` |

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

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|--------|
| 直接在 `skills/` 下放 `git-push.md` | Claude Code 无法识别 | 建 `skills/git-push/SKILL.md` |
| description 只写"做 XX" 不写何时用 | 自动触发率低或误触发 | 三要素齐全 |
| SKILL.md 超过 200 行 | 后半段指令被忽略 | 拆附件，主文件做路由 |
| 用 `commands/` 代替 `skills/` | 旧机制，无附件能力 | 统一用 `skills/` |
| 把 SOP 写在 CLAUDE.md 里 | CLAUDE.md 膨胀，无法按需加载 | 抽到 skill |
| 默认创建到 `~/.claude/skills/` | 污染用户全局配置 | 默认放项目 `.claude/skills/`，明确要全局才放 `~/` |
| skill 内部又调用自己 | 死循环风险 | 路由式 skill 用引用文档，不重新触发 skill |

---

## 完成后自检

- [ ] 文件路径是 `.claude/skills/<name>/SKILL.md`（不是裸 `.md`）
- [ ] frontmatter 含 `name` + `description`（三要素齐全）
- [ ] SKILL.md ≤ 200 行
- [ ] 高风险操作设置了 `disable-model-invocation: true`
- [ ] 没有创建 `~/.claude/` 下任何文件（除非用户明确要求）
