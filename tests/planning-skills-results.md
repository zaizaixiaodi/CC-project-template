# 新增技能简要验收（2026-10-12）

已安装 5 个入口：think、grill-me、grill-with-docs、implement、ponytail，以及 5 个必要依赖：grilling、domain-modeling、tdd、code-review、codebase-design。

| 技能 | 隔离行为结果 |
|---|---|
| think | 根据已有资料提出缺失决策，模拟用户回答后形成可验收方案，未擅自实现 |
| grill-me | 实际完成两轮追问，确认共享理解；该阶段不生成领域文档或代码 |
| grill-with-docs | 读取两项依赖，写入 CONTEXT.md 领域词汇及稳定材料编号 ADR；其他规则未强行生成 ADR |
| implement | 两次真实 RED→GREEN，8 项 unittest 通过；两轴审查均为 0 项问题，完成获授权的隔离本地提交 |
| ponytail | 示例从 18 行缩为 4 行，保留公开函数与错误处理；3 项既有测试和额外输入断言通过 |

10 个新增技能均通过官方 quick_validate（Windows 使用 UTF-8 模式）；用户安装文件与项目源码哈希一致。记录见 planning-skills-format-results.json 和 planning-skills-install-results.json。
当前项目结构检查通过：18 skills、2 角色、MCP TOML 与技能依赖链接。

测试采用独立子代理读取技能并执行模拟用户请求，产物位于被 Git 忽略的 tests/.tmp/skill-evals；不等于所有客户端自动加载行为的完整验收。实现样例未配置类型检查器，py_compile 仅作为语法检查。
源技能未被测试代理修改，未访问真实远端或业务数据。按用户要求止于基本验证，不扩大测试。
