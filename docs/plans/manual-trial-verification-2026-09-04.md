# Project1 真实试跑报告 · 2026-09-04

内部工程候选，不是 0.1.0 发布，也不替代用户价值验收。

## 实际执行边界

- 项目：用户创建的当前工作区 `Project1/project-1`，始终同一份原生工程。
- Godot 4.7.2，GDScript，实际渲染设置 `gl_compatibility`。
- godot-ai 3.2.4，固定 revision `a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e`。
- Codex 实际调用 MCP 创建/修改场景、脚本、输入、CircleShape2D、纹理绑定；MCP 执行运行、
  输入、观察、截图、日志及停止。CLI 只用于 Core 检查、记录和框架测试，不冒充 MCP 玩法验收。
- 内置 imagegen 生成角色原图；归一化为本夹具的 64×64 RGBA PNG。原图、处理记录、来源和
  SHA-256 已保留；许可标为内部评估，不擅自声明 CC0 或已完成商用法律审核。

## 运行记录

| 轮次 | Session / Run | 结果 |
| --- | --- | --- |
| 首次实现 | `project-1@74b7` / `r650553-1` | speed 200，计数 0→1，Target 移除，截图与无错误日志 |
| 增量并重连 | `project-1@2911` / `r82629-1` | speed 240，四方向分别观测，收集成功 |
| 完整记录取证 | `project-1@2911` / `r961837-2` | 当前指纹、四方向、截图和诊断 |
| 过期拒绝后复验 | `project-1@2911` / `r1203103-3` | 恢复源文件后重新运行，最新 Evidence PASS |

中间一次受人工输入干扰的运行不计入通过矩阵。最初短输入未到目标，明确失败后增加移动时长，
没有把未收集状态记作成功。输入使用 render-frame 时间线，**不宣称确定性物理步进**；不支持的
pause / deterministic step / step_until 不做伪模拟。

最新运行：从 (220,300) 开始，上→(220,240)、下→(220,300)、左→(160,300)、右→(220,300)，
继续向右到 (700,300) 时 `items_collected=1`、`target_exists=false`、`speed=240`。
800×560 截图的 `stale_frame=false`，当前运行与编辑器日志没有错误。

## 工程检查

- Python 回归：51 项通过；包括 Windows 管道中文 UTF-8；两个假 Provider 实际经过同一 CLI/Schema/记录/审核路径，覆盖成功、
  超时、能力不足、运行失败、坏素材、旧脚本/PNG、缺截图、错节点及缺 run identity。
- 真实 MCP Godot 测试：4 项通过、0 跳过；节点、输入无重复，视觉与碰撞存在；Dock 加载和刷新
  前后比较所有项目及记录文件哈希，排除 `.godot`、`.git` 和第三方 addons。
- 原始 Advisor / Runtime Probe / Dock smoke 继续由 `scripts/test-framework.ps1` 回归。
- 本轮用 MCP 修改真实脚本一行注释，Core 返回 `stale_evidence` 与非零退出码；恢复后重新运行
  取证通过。合成测试另外覆盖 PNG、素材透明度和截图缺失的拒绝。
- 对真实项目单独加载 Dock 的检查输出 `Source: CURRENT`、`collect-trial · PASS`，且项目文件
  哈希未变。该 headless 检查有 Windows 根证书存储读取警告，不属于游戏运行证据；未隐藏该警告。

## 证据位置与可复验性

项目 `.vibegame/gamemaker/` 包含 environment、conformance、可重建 index 和
`work/collect-trial/` 的 Decision、Query、Production、Asset Spec、Normalized Asset、Binding、
Implementation、Evidence。JSON/Markdown 与哈希元数据进入 Git；`artifacts/` 保存本机原始
截图、原图和工具返回，不进入 Git。

最新截图：`artifacts/run5-collected.png`；输入、状态、日志：`artifacts/run5-observations.json`；
拒绝记录：`artifacts/stale-rejection.json`。这些路径相对于上述项目记录目录。

`doctor --live` 的 ready 表示文件准备、当前连接和有完整制品的历史能力验证；不是“任意任务均完成”。
每次修改仍需 `evidence review --project Project1/project-1 --work collect-trial` 并产生新证据。
从 Git 获取项目但缺少忽略的原图/截图时必须降为证据不足，不自动补造。

## 尚未宣称完成

- 部分 Decision/Production 记录是执行后补录，未宣称已验证一次独立的制品先行 Skill 自动路由。
- 新的自然语言“速度再加 20%”应从当前 240 增至 288，这是下一次用户实际体验的验收。
- 素材艺术质量、玩法手感、语境是否少丢失，由用户确认；尚不晋升或发布公共版本。
