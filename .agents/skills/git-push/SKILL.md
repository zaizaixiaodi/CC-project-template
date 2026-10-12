---
name: git-push
description: 用户明确要求提交或推送当前项目时检查 Git 状态并执行对应操作。不用于自动收尾、覆盖远端或无关仓库。
---
# 提交与推送
- 先运行 git status --short、git branch --show-current、git remote -v、git diff，检查暂存区及未跟踪文件。不要输出含凭据的远端地址。
- 仅暂存本次授权任务相关文件，不使用无差别 git add .；没有改动时不制造空提交。
- 仅要求提交时止于提交；要求推送才执行推送。使用当前分支和已配置 upstream；不存在时确认目标远端与分支后设置，不硬编码 main 或账号。
- 新项目可按授权 git init；不要替换已有 origin 或自动改分支名。目标不明确才询问。
- 使用 Git Credential Manager、SSH 或 gh auth login 的现有认证；不要索要聊天中的 PAT，不把 token 写入 URL/文件/命令。
- 推送失败先诊断；保留现有代理配置。非快进时先 fetch 和比较历史，报告分歧，不自动合并不相关历史、checkout --ours、强推。
- 无网络测试可使用隔离目录中的本地 bare 仓库作为远端，验证提交和推送的真实结果。
