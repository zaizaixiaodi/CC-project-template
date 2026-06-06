---
name: git-push
description: 将当前项目初始化 git 并推送到指定 GitHub 仓库。适用于：首次推送或日常推送到用户账号下的仓库。不适用于：其他账号的仓库、需要 SSH 的场景、已有复杂分支策略的项目。
disable-model-invocation: true
argument-hint: <仓库名，例如 CC-project-template>
---

# git-push

推送当前项目到 GitHub 的完整流程。

## 第一步：收集必要信息

向用户确认以下两项（若通过 `$ARGUMENTS` 已传入仓库名则跳过第 1 条）：

1. **GitHub 仓库地址**（或仓库名）
   - 格式示例：`https://github.com/zaizaixiaodi/CC-project-template.git`
   - 或仅提供仓库名：`CC-project-template`（账号默认为 zaizaixiaodi）

2. **Personal Access Token（PAT）**
   - 提示用户：**token 已记录在 Wolai 笔记中，可直接查取**
   - 若需重新生成：GitHub → Settings → Developer settings → Personal access tokens → Generate new token，勾选 `repo` 权限

## 流程

3. **初始化 git**（若尚未初始化）
   ```
   git init
   ```

4. **暂存所有文件**
   ```
   git add .
   ```

5. **提交**（若已有提交历史则跳过）
   ```
   git commit -m "Initial commit"
   ```

6. **设置 remote**
   ```
   git remote remove origin
   git remote add origin https://<TOKEN>@github.com/zaizaixiaodi/<仓库名>.git
   ```

7. **切换到 main 分支**
   ```
   git branch -M main
   ```

8. **推送（绕过本机代理）**
   ```
   git -c http.proxy="" -c https.proxy="" push -u origin main
   ```

## 冲突处理

若远程已有内容导致推送被拒，执行：

```
git -c http.proxy="" -c https.proxy="" pull origin main --allow-unrelated-histories --no-edit
git checkout --ours <冲突文件>
git add <冲突文件>
git commit -m "Merge: keep local version"
git -c http.proxy="" -c https.proxy="" push -u origin main
```

## 注意事项

- 本机代理为 `127.0.0.1:17890`，推送时必须用 `-c http.proxy="" -c https.proxy=""` 绕过
- 推送完成后建议将仓库设为 Private
