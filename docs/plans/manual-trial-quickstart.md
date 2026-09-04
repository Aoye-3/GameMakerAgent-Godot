# Project1 手动试用接入

状态：内部试用候选已实跑；MCP 编辑、生成角色、四方向移动、收集、速度 +20%、截图、
重连及记录审核已通过。当前玩家速度为 240。工程结果见[试跑报告](manual-trial-verification-2026-09-04.md)。

## 一次性操作

1. 保存并关闭正在编辑 Project1 的其他 Godot 窗口，避免两个编辑器同时写同一项目。
2. 在本仓库 PowerShell 运行以下命令。启动器使用工作区 Godot 4.7.2，并把用户数据和缓存
   指向工作区 `.tools/`；不要再从 Steam 启动本次试用。

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start-trial-godot.ps1
   ```

3. 在 Project Settings → Plugins 中启用 **Godot AI** 与 **GameMaker Context**。
   不点击 Godot AI 的 Configure all，不进行上游升级。确认其 Dock 显示连接状态。
4. 在 Codex 中信任当前工作区并重载 MCP 配置；服务器名称为 `gamemaker_godot_trial`。
   `.codex/config.toml` 仅作用于当前工作区。若客户端仍看不到服务器，重启 Codex 后重新打开
   当前任务，不新建工作树或复制项目。
5. 告知 Agent 已完成。Agent 首先从实际 MCP 工具列举会话，验证绝对路径是当前工作区的
   `Project1/project-1`；这一步通过以前不声称能协作编辑。

准备脚本为 `scripts/prepare-trial.ps1`；`-CheckOnly` 只检查输入，不安装或生成文件。
完整准备会安装固定外部组件和本地目录链接，不启用插件、不改全局配置、不启动游戏。
外部包在 `.tools/providers/`，不是框架源代码；不要提交 Project1 的第三方 addon 链接。

## 实际操作与验收提示词

现在可在同一个 Codex 工作区逐条使用。项目已有实现，“制作功能”应对齐并更新已有对象，
不要另建项目或重复节点。F5 运行，WASD / 方向键移动，接触金色目标；收集后 F8 停止，再 F5 重开。

**制作功能**

> 使用 GameMaker 的 game-delivery，在已打开的 Project1 中制作单场景四方向俯视移动和
> 接触收集。生成一张符合 Asset Spec 的 64×64 RGBA 角色图，检查通过后使用 Godot MCP
> 创建场景、绑定素材、配置输入和碰撞。通过 MCP 运行并输入，验证 items_collected 从 0
> 变为 1、目标消失，保存运行截图和诊断。不要用直接改文件加 CLI 运行冒充 MCP 编辑验收。
> 如果当前功能和合格素材已经存在，复用并复验，不重复生成素材或创建节点。

**增量修改**

> 将玩家移动速度提高 20%，复用已有节点、输入和素材 ID。通过 MCP 修改并复验，保存当前
> revision 的新截图和状态证据，确认无重复节点或漂移引用。

当前速度是 240，因此下一次执行这条提示词应变为 288；已完成的 200 → 240 是工程预演记录。

**复验**

> 使用 evidence-review 检查当前实现、Binding 与证据是否一致。旧截图、缺少运行身份、
> 错误节点或不合规素材不能 PASS；指出最小失败边界，并在修复后重新运行取证。

## 已知的当前限制

- `doctor` 默认只作静态检查，`files_ready` 不代表已安装到 Codex、已连接或可试玩。
- `doctor --project Project1/project-1 --live` 只调用身份/会话/编辑器状态读取，检查已保存的
  conformance 制品哈希；不启动游戏、改场景或代替新的功能复验。
- 项目实际渲染设置已切为 `gl_compatibility`；创建时的 features 标签仍有 Forward Plus，
  以实际 rendering setting 为准。不要仅凭 features 标签判断正在使用的 Renderer。
- Dock 的 Provider 是最近记录，不是持续联网状态；实时连接以 doctor --live 为准。
- 截图、原图与原始日志在忽略的 artifacts；新环境缺少这些文件时审核会如实显示证据不足，
  必须重新生成/归档或运行取证，不能从 Git 中的 PASS 标签推断成功。
- 用户允许内置生图先暂存 C 盘 Codex 目录；项目使用的原图及归一化图已归档到 F 盘。
- 最新卡片完整且可编译，但部分为工程执行后补录；下一轮由你检验 Skill 能否真正减少接线工作。

完整交付门禁见 [里程碑](godot-manual-trial.md)。本文件不能作为 PASS 证据。
