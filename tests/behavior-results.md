# 行为验收结果（2026-10-12，Asia/Shanghai）

执行者：当前会话实际委派的子代理，手动读取 `.codex/agents/workflow-tester.toml` 的角色指令。此结果证明模型读取这些流程后能执行并产生产物；不证明 Codex 原生 TOML 自动发现或 `$skill-name` 自动加载。

## 执行方式与证据

先通过 Get-Content 读取 plan、handoff、devlog、done、git-push 的 SKILL.md，以及 plan/handoff/devlog 模板。模型依据指令编写并执行 `tests/run_behavior.py`，在 `tests/.tmp/behavior/final-run/` 生成真实文件和两个隔离 Git 仓库。脚本是确定性产物检查与隔离操作复现，不是模型调用测试框架。

执行命令：`python tests/run_behavior.py`。本机通过 Python 3.14 绝对路径运行；最终退出码 0。完整 Git 命令、退出码与输出保存在 `tests/.tmp/behavior/final-run/commands.json`。首次 Windows 沙箱执行本地 push 时 Git sh.exe 因 NtCreateDirectoryObject 权限被拒绝；经批准在沙箱外重跑后本地 push 成功。未访问网络远端。

| 用例 | 结果 | 实际证据 |
|---|---|---|
| plan：整理三份会议材料、交付报告 | 通过 | `snapshots/PLAN-created.md` 包含目标、边界、两步实施、两个可核验验收、逐来源核验方法；`materials/` 与 `report.md` 实际生成 |
| handoff：旧目标作废，更新目标与下一步 | 通过 | `snapshots/HANDOFF-old.md` 和 `snapshots/HANDOFF-updated.md`；新文件不含旧目标、少于 80 行，计划仅留一行指针 |
| devlog：同日两轮收尾 | 通过 | 同一个 `devlog/2026-10-12.md` 同时保留第一轮、第二轮，收尾继续追加，无日期分裂 |
| done：全部验收通过，不提交推送 | 通过 | 根 PLAN.md 消失，归档到 `archive/plans/2026-10-12-三份会议材料整理.md`；HANDOFF 不再引用活跃 PLAN；日志追加收尾；`no-commit-evidence.json` 中前后 HEAD 相同 |
| git-push：隔离提交推送本地 bare | 通过 | `push-case/authorized.txt` 仅显式暂存此文件；当前分支保留 `review-feature`；upstream 为 `origin/review-feature`；本地 HEAD 与 bare 的 refs/heads/review-feature 相同 |
| structure-guide：新增 reviewer 的导航 | 通过（读取路由） | 实际读取 SKILL.md → principles.md → guides/subagent.md，定位项目路径 `.codex/agents/<name>.toml`，必填 name、description、developer_instructions；只读 reviewer 可配置 sandbox_mode="read-only"。没有创建无授权源角色 |
| workflow-tester：隔离运行行为用例 | 通过（手动角色委派） | 当前子代理读取角色、技能，执行工具生成上述产物；脚本通过 SHA256 前后比对断言源技能未修改 |
| workflow-reviewer：只读审查 | 通过（手动读取角色） | 读取 workflow-reviewer.toml、AGENTS.md、根 HANDOFF.md 和技能引用。角色含 read-only；审查时根 HANDOFF 快照为占位符，与 AGENTS 的“模板无在途任务”一致（主代理此后更新为实际迁移状态）；done 的提交边界与 git-push 一致。发现 devlog 模板引用错误，报告给主代理后由主代理修复，reviewer 未编辑源文件 |

无提交收尾 HEAD：`3fb5ef84e22db8d2e0ebc2c14c79d6cabe8f1ee9`。
本地推送两端共同 HEAD：`2c865c2de171275fcb7b874c444559cc3ce307cd`。

## 修复与限制

测试中发现 devlog/SKILL.md 最初引用 `templates$devlog-day.md`，真实文件是 `templates/devlog-day.md`。已报告，由主代理修复；最终运行确认源技能哈希不变。首次测试脚本遗漏一次 UTF-8 参数、使用了旧归档路径，均修复后在新的 final-run 隔离目录完整重跑。早期失败目录只用于诊断，不作为通过证据。

原生 skills 自动发现、显式 `$skill-name` 加载、项目 TOML 角色自动注册仍需以仓库作为工作目录的新 Codex 会话验证；当前会话主代理报告原生 CLI 执行因 host policy 拒绝，不能把这里的手动委派表述为该项成功。

重复执行验证：脚本发现 final-run 已存在后创建 run-bc18e6d80cb7，退出码 0、五项行为均通过、源技能哈希不变，未覆盖旧仓库。后续重复运行使用 UUID 新目录。

