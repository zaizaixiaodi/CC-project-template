# 通用原则（所有结构变更前必读）

## 三层架构

| 层 | 机制 | 存什么 |
|---|------|------|
| **Fact 事实层** | `CLAUDE.md` + `rules/` | 项目约定、禁止事项、风格要求 |
| **Procedure 流程层** | `skills/` | 多步骤工作流、SOP |
| **Learning 记忆层** | Harness 自动记忆 `~/.claude/.../memory/` | Claude 自动积累的个人经验（按人、不提交 git、不随项目共享） |

**禁止跨层污染**：把流程塞进 CLAUDE.md、把事实写进 skill，都是高频错误。

**记忆层 ≠ 团队知识库**：记忆层是 per-user、自动维护、不进 repo 的。需团队共享的持久知识不要往这里塞——规范型进 Fact 层（CLAUDE.md/rules），项目专属的描述型知识进 `docs/`（CLAUDE.md 留指针）。

---

## 官方推荐目录结构（速查）

```
project-root/
├── CLAUDE.md                      # 项目指令（每次会话自动加载）
├── CLAUDE.local.md                # 个人覆盖（git 忽略）
└── .claude/
    ├── settings.json              # 权限、hooks、env（团队共享）
    ├── settings.local.json        # 个人设置覆盖（git 忽略）
    ├── rules/<topic>.md           # 主题规则（可带 paths 路径谓词）
    ├── skills/<name>/SKILL.md     # 可调用流程（文件夹结构！）
    ├── agents/<name>.md           # 独立上下文角色（裸 md！）
    └── output-styles/<name>.md    # 输出风格（按需）
```

**最易写错的三处路径**：

- skill 是 `skills/<name>/SKILL.md`（**文件夹** + 内含 SKILL.md），不是 `skills/<name>.md`
- agent 是 `agents/<name>.md`（**裸 md**），不是 `agents/<name>/SKILL.md` 那样的文件夹
- hooks 和 permissions 都写在 `settings.json` **内部**，**不要**单独建 `hooks.json` 或 `permissions.json`

不确定路径就回来对这张表，**不要凭记忆生造**。

---

## 硬约束（任何变更都不得违反）

1. 根目录 `CLAUDE.md` ≤ **200 行**，子目录 `CLAUDE.md` ≤ **30 行**
2. **不使用 `commands/`**——所有可调用流程一律用 `skills/`（commands 是旧机制，无附件能力）
3. 所有生成文件**只能在项目目录内**（`CLAUDE.md`、`.claude/`），**绝不写入 `~/.claude/`**，除非用户明确要求"全局"
4. skill 的 `description` **必须含三要素**：做什么 + 何时用 + 何时不用
5. **优先编辑现有文件**，不要新建重复文件
6. **不写多余注释、说明文档、README**（除非用户明确要求）
7. SKILL.md ≤ **200 行**——详细内容拆到附件文件，主文件做路由

---

## 项目级 vs 全局级

| 范围 | 位置 | 用途 |
|------|------|------|
| 项目级（团队共享） | `.claude/`、`CLAUDE.md` | 团队共用的约定，提交 git |
| 项目级（个人覆盖） | `.claude/settings.local.json`、`CLAUDE.local.md` | 个人偏好，不提交 git |
| 全局级（个人） | `~/.claude/` | 跨所有项目的个人偏好 |

**默认创建到项目级**。除非用户**明确说**"我所有项目都要用"或"这是我个人偏好"，否则不要碰 `~/.claude/`。即使要全局，也要**先和用户确认**。

---

## 信息存放优先级（从高到低）

同一条信息能放多处时，按这个顺序选最具体的位置：

1. `settings.json` 强制执行（`permissions`、`hooks`）— 适合"不可违反"的红线
2. `.claude/rules/` 按文件类型触发的规则（带 `paths:` 字段）
3. 子目录 `CLAUDE.md` — 按工作模块触发
4. 根目录 `CLAUDE.md` — 全项目通用事实
5. `.claude/skills/` 按需加载的多步骤流程
6. `.claude/agents/` 需要独立上下文的专精角色

**最小成本原则**：能塞进现有文件就不新建；能放更具体的位置就不放根。
