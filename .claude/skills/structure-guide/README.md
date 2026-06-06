# structure-guide

项目结构变更的**导航 skill**。每次要写/改 CLAUDE.md、新建 skill、新建 subagent、新建 rule、配置 hooks/permissions 时，引导 Claude 先读对应 guide 再动手——避免凭记忆瞎写、文件膨胀、目录错乱。

---

## 怎么用

### 方法一：CLAUDE.md 引用（推荐）

在项目根目录 `CLAUDE.md` 顶部加这一段：

```markdown
## 结构变更前必读
创建/修改 CLAUDE.md、skill、subagent、rule、hooks 时，
先读 .claude/skills/structure-guide/SKILL.md，按其中的路由跳到对应 guide。
```

之后任何结构性变更，Claude 都会自动加载本 skill。

### 方法二：手动触发

```
/structure-guide
```

---

## 目录说明

- `SKILL.md`：路由表，根据用户意图跳转
- `principles.md`：所有 guide 共用的核心原则（每个 guide 都会先读这个）
- `guides/*.md`：六大类结构变更的详细指南

---

## 迁移到新项目

```bash
cp -r .claude/skills/structure-guide /path/to/new-project/.claude/skills/
```
