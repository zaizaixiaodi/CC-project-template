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

附件可选结构（对齐官方 Agent Skills 约定）：
```
.claude/skills/<skill-name>/
├── SKILL.md           ← 主入口，必需
├── scripts/           ← 可选：确定性操作的可执行代码（抽 PDF、填 docx 等），由 SKILL.md 调用而非贴进正文
├── references/        ← 可选：按需加载的参考文档/schema/示例（内容多时用文件夹；单文件可叫 reference.md）
└── assets/            ← 可选：会拷进产出物的文件（模板、图标、字体）
```

> 命名说明：本仓库现有 skill 用 `templates/` 装模板，等价于官方 `assets/` 的模板子集——沿用即可，不必改名。新写涉及"代码"的 skill 时记得用 `scripts/`：能用脚本确定性完成的（格式转换、批量替换），别让模型每次现推，省上下文也更可靠。

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

先过这组**格式硬规则**（取自官方 skill-creator 的 `quick_validate.py`，本质一致，是机器可校验的）：

- [ ] 目录下有 `SKILL.md`，且以 `---` YAML frontmatter 开头
- [ ] frontmatter 含 `name` 与 `description` 两个必填项
- [ ] `name` 是 kebab-case（小写字母/数字/连字符）、≤64 字符、不以连字符开头结尾、无连续连字符
- [ ] `description` 不含尖括号 `<` `>`、≤1024 字符
- [ ] description 三要素齐全（做什么 / 何时用 / 何时不用）

再过本仓库的 skill 专属项：

- [ ] 高风险操作设了 `disable-model-invocation: true`
- [ ] 接受参数的写了 `argument-hint`，正文用 `$ARGUMENTS`/`$1`
- [ ] 代码逻辑放进了 `scripts/`，没贴进 SKILL.md 正文
- [ ] 结构/行数等通用硬约束已对照 `principles.md`

> 注意：官方校验器只认 `name`/`description`/`license`/`allowed-tools`/`metadata`/`compatibility` 六个键，会把 Claude Code 专属的 `disable-model-invocation`/`argument-hint`/`user-invocable` 判为"非法键"。这几个在 Claude Code 里是合法的——**别据此删它们**，也别直接拿官方脚本验本仓库的 skill。
