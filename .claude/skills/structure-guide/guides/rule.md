# 写 rule 指南

## 何时用本指南

- 用户要建"只在改特定类型文件时才生效"的规则
- 根 CLAUDE.md 逼近 200 行需要减负
- 用户要按主题拆分指令（如把"测试规范"独立成文件）

## 何时不用

- 规则按"目录范围"触发（如只在 `contracts/` 下） → 跳 `subdirectory.md`（用子目录 CLAUDE.md 更合适）
- 规则是"必须物理拦截"的强制执行 → 跳 `hooks.md`（用 `settings.json` permissions）
- 规则是多步骤工作流 → 跳 `skill.md`

---

## 核心方法论

### rules 是引导，不是强制执行

`rules/` 下的文件是 Claude **读取并尽力遵守**的指令，和 CLAUDE.md 同性质——不是 settings.json 的物理拦截。需要硬约束就用 `hooks` 或 `permissions`，跳 `hooks.md`。

### 两种 rules

**类型一：无 `paths:`（等同 CLAUDE.md，每次会话加载）**
```markdown
# .claude/rules/writing-style.md
不使用被动语态。法律意见书结尾必须有"综上所述"总结段落。
```

**类型二：有 `paths:`（只在 Claude 读取匹配文件时才加载）**
```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API 设计规则
- 所有 endpoint 必须用 Zod schema 校验输入
- 返回 `{ data: T } | { error: string }` 形状
```

### rules/ vs 子目录 CLAUDE.md

| 触发维度 | 用什么 |
|---------|--------|
| 按文件类型（`.tsx`, `.md`） | `rules/` + `paths:` |
| 按目录范围（`contracts/`） | 子目录 CLAUDE.md |
| 全局通用 | 根 CLAUDE.md（不必建 rule） |

---

## 决策规则

| 情况 | 方案 |
|-----|------|
| 规则只对某类文件有效 | 类型二（有 `paths:`） |
| 规则按主题拆分但全局生效 | 类型一（无 `paths:`） |
| CLAUDE.md 接近 200 行 | 把次核心内容迁到 rules/ 类型一 |
| 规则全项目通用且少（< 5 行） | 留在 CLAUDE.md，不必单独建 rule |
| 规则需要 Claude **必须**执行 | 不要用 rules，跳 `hooks.md` 用 permissions/hooks |

### paths 语法（glob）

```yaml
paths:
  - "**/*.test.ts"          # 所有测试文件
  - "**/*.test.tsx"
  - "src/api/**/*.ts"       # API 目录下的所有 ts
  - "contracts/**/*.{md,docx}"  # 多扩展名
```

---

## 模板

### 类型一：无 paths（全局加载）

`.claude/rules/<topic>.md`：

```markdown
# <主题名>

- <规则 1>
- <规则 2>
- <规则 3>
```

### 类型二：有 paths（条件加载）

`.claude/rules/<topic>.md`：

```markdown
---
paths:
  - "<glob 模式 1>"
  - "<glob 模式 2>"
---

# <主题名>

- <规则 1>
- <规则 2>
```

---

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|--------|
| 用 rule 写硬约束（如"绝不允许 rm"） | rule 是引导，Claude 可能违反 | 用 `settings.json` permissions.deny |
| paths 写反了（用法 `path:` 单数） | 字段失效，规则不触发 | 必须是 `paths:` 复数 + 列表 |
| paths 用绝对路径 | 不匹配 | 用相对项目根的 glob |
| 把多步骤流程塞进 rule | 流程不应作为事实存储 | 抽成 skill |
| 同一规则在 CLAUDE.md 和 rules/ 都写 | 浪费 token | 二选一 |
| rule 文件超 50 行 | 失去"主题化"意义 | 进一步拆分主题 |

---

## 完成后自检

- [ ] 文件路径是 `.claude/rules/<topic>.md`
- [ ] 如果是类型二，frontmatter 用 `paths:`（复数）+ 列表
- [ ] 每条规则具体可验证（5 秒内可判断）
- [ ] 文件 ≤ 50 行（超过说明主题太宽，再拆）
- [ ] 没和 CLAUDE.md 内容重复
