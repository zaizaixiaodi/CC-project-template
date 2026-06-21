# 把脚手架改造成 Claude Code 插件（Plugin）——设计方案

> 性质：设计/参考文章，非执行记录。本文只规划"怎么改"，不代表已经改了。
> 缘起：现有 `project-template` 是整包复制型脚手架，想改成 AI 时代更优雅的、可分享的分发形态。

---

## 一、要解决的困惑

直觉是"把整个脚手架做成一个 skill"，但很快卡住：**这个 skill 本身又装着好几个 skill 和模板，skill 怎么能装 skill？**

结论先行：**它不该是 skill，而该是 plugin（插件）。**

- Claude Code 里 **skill 不能嵌套**，"一个 skill 装很多 skill"在机制上不成立。
- 装"多个 skill + 模板 + 配置"的原生容器叫 **plugin**。
- 分发 plugin 的渠道叫 **marketplace**——本质就是一个 git 仓库，里面放一份 `.claude-plugin/marketplace.json` 清单。

所以"脚手架 skill 化"的准确说法是"**脚手架 plugin 化**"。

---

## 二、一个绕不过去的限制，决定了整体设计

plugin 能装 skill、能带模板、能带权限配置，但有一条硬限制：

> **plugin 无法自动往项目里注入"始终生效"的文件**，尤其是 `CLAUDE.md`。

因为 `CLAUDE.md` 是每次会话从磁盘真实读取的；plugin 的 skill 是"按需加载"的，hook 也无法在会话启动时凭空造出一份 CLAUDE.md 约束。**始终生效的约束，只能靠项目里真实存在的 CLAUDE.md。**

这条限制把脚手架的内容干净地劈成两半：

| 类别 | 例子 | 归宿 |
|---|---|---|
| 方法论 / 流程能力（按需加载就行） | structure-guide、plan、handoff、done、git-push | **进 plugin**，装一次，所有项目可用 |
| 每个项目必须真实落地的文件 | `CLAUDE.md` 治理段、`HANDOFF.md` | **靠一个 `init` 命令现场生成**到当前项目 |

一句话：**plugin 负责"能力"，`/init` 负责"在新项目落地文件"。**

---

## 三、推荐方案：单 plugin + 自有 marketplace

### 3.1 目标仓库结构

新建一个 git 仓库当 marketplace（建议名 `cc-workflow-marketplace`），内含一个 plugin（建议名 `cc-workflow`，对外分享时可换更通用的名字）：

```
cc-workflow-marketplace/                  # ← 这个 git 仓库就是 marketplace
├── .claude-plugin/
│   └── marketplace.json                  # 列出本仓库提供哪些 plugin
├── plugins/
│   └── cc-workflow/                      # ← plugin 本体
│       ├── .claude-plugin/
│       │   └── plugin.json               # plugin 清单（只有它放 .claude-plugin/ 内）
│       ├── skills/                       # 注意：放 plugin 根，不是 .claude-plugin/ 里
│       │   ├── structure-guide/          # 原样搬：SKILL.md + principles.md + guides/ + README.md
│       │   ├── plan/                     # + templates/PLAN.md
│       │   ├── handoff/                  # + templates/HANDOFF.md
│       │   ├── done/
│       │   ├── git-push/
│       │   └── init/                     # 【新增】落地 CLAUDE.md + HANDOFF.md
│       ├── templates/
│       │   └── CLAUDE.md                 # 【新增】治理段模板（原根 CLAUDE.md 改造而来）
│       └── settings.json                 # git 权限白名单（作为安装后默认值）
└── README.md                             # 安装与使用说明（分享给别人看）
```

> 官方硬规矩：`.claude-plugin/` 里**只能放 `plugin.json`**；`skills/`、`commands/`、`agents/`、`hooks/` 都必须放在 plugin 根目录下。

### 3.2 改造后用户怎么用

```
# 一次性（每台机器 / 每个用户装一次）
/plugin marketplace add zaizaixiaodi/cc-workflow-marketplace
/plugin install cc-workflow            # 选 user 作用域 = 所有项目可用

# 每个新项目一次
/cc-workflow:init                      # 在当前项目落地 CLAUDE.md + HANDOFF.md
```

之后 plan / handoff / done / git-push / structure-guide 在任何项目都能按需自动加载。
**skill 升级只要 `/plugin marketplace update`，所有项目同步**——这正是整包复制做不到的。

---

## 四、从"整包复制"迁到"plugin"，必须处理的 5 件事

这 5 点是迁移的真正难点，不是简单挪文件夹就完事。

### 1. 新增 `init` skill（核心新增件）

- `disable-model-invocation: true`：它要写文件、属高影响操作，**只允许用户手动 `/cc-workflow:init` 触发**，不让 Claude 自动跑。
- 流程：
  1. 项目无 `CLAUDE.md` → 从 `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.md` 复制；**已存在 → 先问用户**是否把治理段追加进去，绝不盲目覆盖用户已有的 CLAUDE.md。
  2. 项目无 `HANDOFF.md` → 从 `${CLAUDE_PLUGIN_ROOT}/skills/handoff/templates/HANDOFF.md` 复制到根目录。
  3. 提示：git 权限白名单已由 plugin 的 `settings.json` 提供（或按需写 `.claude/settings.local.json`）。
- description 三要素：做什么 = 在当前项目落地 workflow 项目级文件；何时用 = 新项目首次启用本工作流；何时不用 = 这些文件已存在的项目（避免覆盖）。

### 2. CLAUDE.md 模板里的 structure-guide 引用必须改写

现根 `CLAUDE.md` 写死了一条路径：

> 先读 `.claude/skills/structure-guide/SKILL.md`

但装了 plugin 的项目里**这个本地路径根本不存在**——skill 实际躺在 plugin 缓存目录里。所以模板 `templates/CLAUDE.md` 要改成**按 skill 名调用**，而不是写文件路径：

> 先按 structure-guide skill（`/cc-workflow:structure-guide`）的路由处理

这是最容易被忽略、却一定会踩的坑。

### 3. 凡是"复制模板"的 skill，路径要改用 `${CLAUDE_PLUGIN_ROOT}`

涉及 handoff（复制 HANDOFF.md）、plan（复制 PLAN.md）、新增的 init（复制 CLAUDE.md / HANDOFF.md）。

现在写的是相对路径 `templates/HANDOFF.md`。打包成 plugin 后，skill 运行时的相对路径基准变了（指向 plugin 缓存），**必须改成** `${CLAUDE_PLUGIN_ROOT}/skills/<name>/templates/<file>`，否则复制会找不到文件。

### 4. skill 之间的相互引用

done→handoff/plan/git-push、handoff→plan、plan→handoff，这些都是**正文里的文字引用**（"按 handoff skill 的完成归档流程…"）。Claude 靠语义就能找到对应 skill，基本不用改。稳妥起见可以在正文里提一次命名空间名（`/cc-workflow:handoff`），但不是必须。

### 5. 权限与 settings

把现在 `settings.local.json` 里的 git 白名单，迁成 plugin 根目录的 `settings.json`，作为安装后的**默认权限**，这样用户不必每个项目重配一遍 git 权限。

---

## 五、待迁移文件映射表（现状 → plugin）

| 现状 | 迁往 | 改动 |
|---|---|---|
| `.claude/skills/structure-guide/`（全套） | `plugins/cc-workflow/skills/structure-guide/` | 原样 |
| `.claude/skills/{plan,handoff,done,git-push}/` | `plugins/cc-workflow/skills/同名/` | 模板路径改 `${CLAUDE_PLUGIN_ROOT}` |
| 根 `CLAUDE.md`（治理段） | `plugins/cc-workflow/templates/CLAUDE.md` | structure-guide 引用改 skill 调用式 |
| 根 `HANDOFF.md` / handoff 的模板 | `skills/handoff/templates/HANDOFF.md`（保持原位） | 由 init 引用它 |
| `settings.local.json` git 白名单 | `plugins/cc-workflow/settings.json` | 作为默认权限 |
| —（新增） | `skills/init/SKILL.md` | 新写 |
| —（新增） | `.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、marketplace `README.md` | 新写 |

清单文件要点：

- **`plugin.json`**（最小集）：`name` / `description` / `version` / `author`。
- **`marketplace.json`**：`name` / `owner` / `plugins[]`，其中每个 plugin 项写 `name` + `source: "./plugins/cc-workflow"` + `description` + `version`。

---

## 六、可选增强（先不纳入，列为后续）

- **SessionStart hook**：会话一开始自动提醒"先读 HANDOFF.md"。但"始终生效"已经由 init 写出的真实 CLAUDE.md 保证了，hook 只是加固，非必需。
- **原 `project-template` 仓库去留**：marketplace 上线后它成为主入口，旧的整包模板可以保留为镜像或直接归档（沿用此前"归档不删、留个念想"的偏好）。

---

## 七、日后真正执行时怎么验证

1. **本地装**：`/plugin marketplace add ./cc-workflow-marketplace` → `/plugin install cc-workflow`。
2. **空目录测 init**：新建空文件夹起 Claude，跑 `/cc-workflow:init`，确认生成的 `CLAUDE.md`（治理段 + 多轮开发段）与 `HANDOFF.md` 内容正确、structure-guide 引用能解析到 plugin skill 而不是死路径。
3. **测模板复制**：确认 handoff / plan 复制模板时 `${CLAUDE_PLUGIN_ROOT}` 正确解析，不再依赖本地 `templates/`。
4. **测联动**：触发 handoff（会话起）、`/cc-workflow:done`、`/cc-workflow:plan`，确认命名空间下 skill 之间仍能互相找到。
5. **测分享**：把 marketplace 推上 GitHub，换一台环境用 `/plugin marketplace add zaizaixiaodi/cc-workflow-marketplace` 复现安装。

---

## 七点五、更简的备选：一个"生成器"skill（待脚手架稳定后再考虑）

> 记录于讨论中，**暂不执行**——这个文件夹本身还没实测过效果，等用顺、稳定了再谈 skill 化。

比 plugin 更轻的思路：**不分发"一堆现成的东西"，而是分发一个 skill，让它把这套东西"写进"当前项目**（即"引导去建立"而非"直接给成品"）。

绕不开的前提同上：始终生效的约束只能靠项目里真实存在的 CLAUDE.md，所以**每个新项目总得有人写文件**。于是"做成一个 skill"的准确含义 = 一个 skill，职责就是把 CLAUDE.md + HANDOFF.md + 那几个 skill 写进当前项目。把它放在 `~/.claude/skills/` 下即全局可用，**完全不需要 marketplace**。（会写 `~/.claude/`，违反脚手架"禁写全局"铁律，但那条有"用户明确要全局则可"的豁免，正好适用。）

**必须避开的陷阱**：别把 5 个 skill 揉成一个 skill 的正文。那样会丢掉每个 skill 各自的自动触发（handoff 在会话起、plan 在复杂需求、structure-guide 在结构变更、done/git-push 手动）——靠的正是各自独立的 `description`。正确做法是**生成器 skill 写出那几个独立的 skill 文件**，触发粒度全保住。

形态：
```
~/.claude/skills/setup-dev-workflow/      ← 唯一要分发的东西
├── SKILL.md                              ← 被调用时把下面这些写进 cwd
└── templates/
    ├── CLAUDE.md
    ├── HANDOFF.md
    └── skills/{plan,handoff,done,structure-guide,git-push}/
```

**生成器 skill vs plugin 怎么选**：

| | 一个生成器 skill | plugin + marketplace |
|---|---|---|
| 机制复杂度 | 低（扔进 `~/.claude/skills/`） | 高（维护 marketplace 仓库） |
| 落地的 skill | 真文件，可逐项目改 | 在 plugin 缓存，所有项目共用一份 |
| 升级同步 | 不回溯老项目 | `/plugin update` 全同步 |
| 分享给别人 | 让对方拷你的 skill 文件夹（略糙） | 对方 `/plugin install`（更干净） |

判断：**"主要自己用、每类活儿（合同/投标/PPT）工作流还不一样"→ 生成器 skill 更对路**（本就逐项目定制，plugin 的"自动同步一份"价值有限；生成器写出真实文件，随意改）。代价：改了模板不回溯老项目——但老项目都做完了，无所谓。**只有"分享给别人且要持续推送更新"成硬需求时，plugin 才值那套机器。** 两者不冲突：生成器 skill 日后想分享，随时能再包一层塞进 plugin。

---

## 八、一句话总结

把"整包复制的脚手架"拆成两层：**方法论与流程进 plugin（装一次、处处可用、可同步升级、可分享）**，**每个项目必须落地的 CLAUDE.md / HANDOFF.md 靠 `/cc-workflow:init` 现场生成**。这就是"脚手架在 AI 时代的优雅形态"。
