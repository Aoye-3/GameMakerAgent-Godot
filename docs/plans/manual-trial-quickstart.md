# Project1 手动试用接入

状态：组件已准备；真实 MCP 连接、编辑、截图与双轮验收仍待完成。

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

以下供真实连接后逐条使用，不是已经通过的测试报告。

**制作功能**

> 使用 GameMaker 的 game-delivery，在已打开的 Project1 中制作单场景四方向俯视移动和
> 接触收集。生成一张符合 Asset Spec 的 64×64 RGBA 角色图，检查通过后使用 Godot MCP
> 创建场景、绑定素材、配置输入和碰撞。通过 MCP 运行并输入，验证 items_collected 从 0
> 变为 1、目标消失，保存运行截图和诊断。不要用直接改文件加 CLI 运行冒充 MCP 编辑验收。

**增量修改**

> 将玩家移动速度提高 20%，复用已有节点、输入和素材 ID。通过 MCP 修改并复验，保存当前
> revision 的新截图和状态证据，确认无重复节点或漂移引用。

**复验**

> 使用 evidence-review 检查当前实现、Binding 与证据是否一致。旧截图、缺少运行身份、
> 错误节点或不合规素材不能 PASS；指出最小失败边界，并在修复后重新运行取证。

## 已知的当前限制

- `doctor` 默认只作静态检查，`files_ready` 不代表已安装到 Codex、已连接或可试玩。
- `provider_connected` / `conformance_passed` 当前未探测时为 null，`ready` 为 false。
- 项目创建时选择了 Forward Plus；真实连接后按已确认计划切为 Compatibility。
- Core 的素材记录、Evidence revision、真实项目格式解析和 Dock 详细展示尚待下一批实现。

完整交付门禁见 [里程碑](godot-manual-trial.md)。本文件不能作为 PASS 证据。
