# 根 AGENTS.md

用于全项目指令。模块规则见 [子目录](subdirectory.md)，多步骤流程见 [skill](skill.md)。

保留项目定位、实际工作路径、常用验证命令和可验证的约定。详细业务知识放文档，根文件留下指针。不要为了凑条数杜撰禁止事项。

```markdown
# 项目名称

## 项目定位
一句话说明项目用途。

## 工作约定
- 列出已确认的项目约定。

## 验证
- 写入实际存在的测试或检查命令。

## 文档与流程
- 项目背景：docs/project-context.md
- 可复用流程：.agents/skills/
```

创建前检查同目录 `AGENTS.override.md`；它会优先于 `AGENTS.md`，避免编辑了未被加载的文件。用新会话询问加载的指令来源验证。

来源：[官方 AGENTS.md 指南](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。
