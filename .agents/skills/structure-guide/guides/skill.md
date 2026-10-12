# Codex skill

用于需要重复执行的流程。项目路径为 `.agents/skills/<name>/SKILL.md`，显式调用使用 `$skill-name`。

```markdown
---
name: review-draft
description: 审查用户提供的草稿并给出修改建议，适用于定稿前检查，不适用于创建全新草稿。
---

# 草稿审查

读取用户提供的草稿，按实际问题输出修改建议与位置。
```

入口保留关键决策与输出要求；详细参考按需链接，确定性操作放 `scripts/`，产出模板放 `assets/` 或既有 `templates/`。

`name` 用小写字母、数字和连字符，目录名与之一致。description 应明确能力和触发场景，必要时注明排除边界。

不要使用旧工具的 `disable-model-invocation`、`user-invocable`、`argument-hint`、`$ARGUMENTS` 或 `$1` 约定；输入在对话中描述并由流程读取。

只有用户要求仅显式调用时，配置 `agents/openai.yaml`：

```yaml
policy:
  allow_implicit_invocation: false
```

验证 frontmatter、附件路径和脚本执行，再用真实请求检查发现与调用。高风险动作的授权与自动发现是两件事，不要混为一谈。

来源：[官方技能指南](https://learn.chatgpt.com/docs/build-skills)。
