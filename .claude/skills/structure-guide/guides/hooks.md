# 配置 hooks / permissions 指南

## 何时用本指南

- 用户要"物理拦截"某些操作（不是"提醒 Claude 别做"，是"做不了"）
- 用户要在某个操作前/后**自动执行**某些动作
- 用户要设置允许/拒绝的工具调用

## 何时不用

- 用户要写"建议性约定" → 跳 `claude-md.md`（CLAUDE.md 是引导，不是强制）
- 用户要写"按文件类型触发的规则" → 跳 `rule.md`
- 用户要写多步骤工作流 → 跳 `skill.md`

---

## 核心方法论

### settings.json 是强制执行，CLAUDE.md 是引导

| 机制 | 性质 | Claude 是否能"忽略" |
|------|------|---------------------|
| `CLAUDE.md` / `rules/` | 引导，尽力遵守 | 可能忽略（极端情况下） |
| `settings.json` 的 `permissions` / `hooks` | 系统强制执行 | **不能**绕过 |

**判断准则**：能容忍"偶尔违反"就用 CLAUDE.md/rules；不能容忍就用 settings.json。

### 三个 hook 时机

| 事件 | 触发时机 | 典型用途 |
|------|---------|---------|
| `PreToolUse` | 工具调用前 | 拦截危险操作、要求确认 |
| `PostToolUse` | 工具调用后 | 自动格式化、自动验证、自动通知 |
| `Stop` | Claude 完成本轮回复后 | 发完成通知、自动保存状态 |

### 配置存放位置

| 位置 | 范围 | 是否提交 git |
|------|------|------------|
| `.claude/settings.json` | 项目（团队共享） | 是 |
| `.claude/settings.local.json` | 项目（个人） | 否（自动 gitignored） |
| `~/.claude/settings.json` | 跨所有项目 | 否（用户个人） |

**默认项目级**。除非用户明确说"我所有项目都要用"，才放 `~/.claude/`。

---

## 决策规则

| 情况 | 方案 |
|-----|------|
| 绝对禁止某操作 | `permissions.deny` |
| 允许某操作不再询问 | `permissions.allow` |
| 操作前需要拦截判断 | `hooks.PreToolUse` |
| 操作后自动格式化/验证 | `hooks.PostToolUse` |
| 回复完成后自动触发 | `hooks.Stop` |
| 团队共享 | `.claude/settings.json` |
| 个人偏好 | `.claude/settings.local.json` |

### Bash 权限通配符

```
Bash(npm test *)       # 匹配任何以 "npm test" 开头的命令
Bash(git log *)        # 匹配任何 git log 子命令
Bash(rm -rf *)         # 匹配任何 rm -rf
```

---

## 模板

### 基础 permissions

`.claude/settings.json`：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test *)",
      "Bash(npm run *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)"
    ]
  }
}
```

### PostToolUse hook（编辑后自动格式化）

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}
```

### PreToolUse hook（高风险操作前确认）

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo '即将执行命令，请审核' && read -p '继续？(y/n) ' yn && [ \"$yn\" = \"y\" ]"
      }]
    }]
  }
}
```

---

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|--------|
| 把"硬约束"写在 CLAUDE.md 而非 settings.json | Claude 可能忽略 | 不可妥协的红线放 `permissions.deny` |
| permissions 数组里漏了 `Bash(...)` 包装 | 规则不生效 | 必须 `Bash(命令模式)` |
| matcher 不写或写错 | hook 在所有工具上都触发 | 用 `Edit|Write` 等精确 matcher |
| hook command 失败没处理 | 默默失败，行为不可预期 | 加错误处理或 `on_failure: warn` |
| 把个人偏好写进 `.claude/settings.json` 并提交 | 污染团队 | 用 `.claude/settings.local.json` |
| 给 Claude 写到 `~/.claude/settings.json` 而没和用户确认 | 改了用户全局配置 | 默认 `.claude/settings.json`，全局必须用户明确同意 |

---

## 完成后自检

- [ ] 路径是 `.claude/settings.json`（团队共享）或 `.claude/settings.local.json`（个人）
- [ ] permissions 用 `Bash(...)` 包装命令模式
- [ ] hook 含正确的 `matcher`
- [ ] 没有未经用户确认就写入 `~/.claude/`
- [ ] 红线规则真的不能容忍违反（否则可降级到 CLAUDE.md）
