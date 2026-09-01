# Claude Code Game Studios 与 godot-ai 集成评估

## 状态与范围

Research snapshot，查询日期 2026-09-01。本报告评估两个外部项目如何与
GameMakerAgent 框架、TapTapGameJam 原生 Godot 项目和历史 VibeGame 能力结合，
不代表已经选择依赖或完成集成。

本报告聚焦 GameStudio 与 godot-ai。后续对 VibeGame、Godogen、Xenodot、Godot
Gamestudio 和 OpenGame 的横向比较，以及 Production Bridge 结论，见
[Agentic 游戏生产框架对比与 GameMaker 架构结论](agentic-game-production-architecture-study.md)。
Task 1.0 完成后的逐文件采用结论见
[核心竞品源码吸收清单](core-source-intake.md)；本报告中早期访问状态与数量只保留为调研历史，
不再作为当前 intake 状态。

本地研究快照保存在当前仓库的 Git research refs 中，没有创建额外 checkout、
worktree 或项目副本：

| 请求项目 | 本地 ref | revision | 说明 |
| --- | --- | --- | --- |
| `Aoye-3/godot-ai` | `research/godot-ai/main` | `a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e` | 与 `hi-godot/godot-ai` 当前 `main` HEAD 相同 |
| `Aoye-3/Claude-Code-Game-Studio` | 不可访问 | 不可确认 | 公开 Git 和本机失效的 GitHub 凭据均返回不可用 |
| `Donchitos/Claude-Code-Game-Studios` | `research/claude-code-game-studios/main` | `984023ddac0d5e27624f2baacde6105e45de375f` | 仅作为可能上游的结构研究基线，不能代替 Aoye-3 fork 的差异审计 |

上游来源与许可证：

- [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)：MIT。
- [Godot AI](https://github.com/hi-godot/godot-ai)：MIT；本次快照自报版本 3.2.4。
- [Godot EditorPlugin](https://docs.godotengine.org/en/stable/classes/class_editorplugin.html)、
  [EngineDebugger](https://docs.godotengine.org/en/stable/classes/class_enginedebugger.html)：
  Godot 官方扩展与调试能力边界。

## 结论

两个项目与 GameMakerAgent 的关系不是“二选一”，而是位于不同层：

| 项目 | 实际角色 | 推荐采用方式 | 不应承担的职责 |
| --- | --- | --- | --- |
| Claude Code Game Studios | 组织治理、文档模板、阶段门禁、角色路由 | 选择性提炼少量流程模式 | 不作为运行时、不整包复制 49 个角色和 73 个 Skill |
| godot-ai | Godot 编辑器与运行控制后端 | 作为 Runtime Adapter 的候选 provider 实测 | 不直接成为 Agent 角色协议，不向所有 Agent 暴露全部写工具 |
| GameMakerAgent | 生产语义、稳定契约、逻辑职责、证据、晋升门禁 | 保持权威来源 | 不保存具体游戏实现和资产 |
| TapTapGameJam | 原生 Godot 游戏和项目事实来源 | 先落地最小候选适配与验证场景 | 不提前承担跨项目兼容性 |

推荐结论是：

1. **不合并三套框架。** GameMakerAgent 保持控制契约，TapTapGameJam 保持项目真实源。
2. **把 godot-ai 放在可替换 provider 层。** 首轮只映射已需要的运行能力，不让
   Player、Reviewer 或 Maker 依赖 `project_run`、`game_manage` 等上游工具名。
3. **从 Game Studios 抽取知识，不抽取组织规模。** Orchestrator、Maker、Player、Reviewer
   作为逻辑职责按需组合；专业角色只在任务确有取舍时临时启用。
4. **先在同一 runtime probe 上做黑盒对比。** godot-ai 应加入现有 MCP 候选矩阵，
   但在 pause、单步推进和有界语义观察缺口未解决前，不应直接胜出。

## 当前三个系统的事实边界

### GameMakerAgent

当前仓库已经定义 Runtime Adapter、Evidence Bundle、Promotion Manifest 和双仓边界，
但尚未实现首个 Godot provider。它是稳定语义的拥有者，而不是具体 MCP 的包装目录。

### TapTapGameJam / 历史 VibeGame

`F:\.Vibegame` 当前同时包含两类事实：

- `game/` 是原生 Godot 4.7.2 项目真实源，已经有 `runtime_probe`、命名输入
  `verify_trigger`、`gamemaker_watch` 和 `_gamemaker_state()` Draft 0.1。
- `src/` 是历史 VibeGame 提炼来源，已有 Agent 角色、任务编排、Phaser RuntimeBridge、
  输入、暂停/继续、快照、截图、日志和证据工作流。

VibeGame 当前角色链路已经是 `architect -> programmer -> auditor -> player`，并有 lead、
task state、消息、停止 Hook 和 Self-Evolve。它的主要缺口不是“没有更多角色”，而是
Godot provider、统一证据信封和跨引擎契约尚未落地。

另一个明确冲突是历史 VibeGame 的任务 CLI 支持 Git worktree；当前仓库最高优先级规则
禁止 worktree，因此任何复用都必须固定为同目录分支或直接在项目分支工作。

## Claude Code Game Studios 客观评估

### 已验证的结构

本地 v1.0.0 快照包含：

- 49 个 Agent 定义；
- 73 个 Skill；
- 12 个 Claude Code Hook；
- 11 组路径规则；
- 40 个文档模板；
- Concept、Systems Design、Technical Setup、Pre-Production、Production、Polish、
  Release 七阶段目录。

其核心机制是文件驱动治理：GDD、ADR、Control Manifest、Epic、Story、Sprint、测试证据
和 Director Gate 相互引用。`dev-story` 会加载 story、TR registry、ADR、控制清单和引擎
偏好，再路由程序员与引擎专家；`story-done` 和 `gate-check` 负责独立审核与人工确认。

### 值得提炼

| 模式 | 对 GameMakerAgent 的价值 | 建议形态 |
| --- | --- | --- |
| 专业讨论与方案质疑 | 在高成本实现前暴露玩法、体验和范围风险 | 显式调用的 Studio Advisor，不做阶段检测 |
| 任务上下文包 | 让实现只读取当前需求、ADR、约束和验收 | 对齐现有 `prd.md` / `plan.md` / Evidence Bundle |
| Maker 与 Reviewer 分离 | 避免实现者自证完成 | 保留最小逻辑职责，不强制创建四个 Agent |
| 证据类型随任务类型变化 | 逻辑、集成、视觉不应使用同一种验收 | 写入 Evidence Bundle profile 或审核规则 |
| Session recovery Hook | 在上下文压缩或会话恢复时保留任务状态 | 改写为跨客户端 Python/结构化状态机制 |
| Gate 是建议、人工做最终决定 | 适合玩法手感、艺术方向和架构升级 | 继续使用人工 checkpoint |

### 不建议直接采用

1. **角色规模过大。** 49 个角色增加路由、上下文、冲突处理和成本；当前项目最缺的是
   可靠运行闭环，不是更细的岗位名称。
2. **Claude Code 强绑定。** Skill 直接使用 `Task`、`AskUserQuestion`、Claude 模型 ID、
   `.claude/settings.json` 和 Claude Hook 事件，不能直接成为跨 Codex/Claude 的框架契约。
3. **目录契约过重。** 它假定 `design/`、`production/`、`src/`、`tests/` 等目录；直接覆盖
   TapTapGameJam 会与 `docs/project/`、`game/` 和双仓文档边界冲突。
4. **Hook 主要是 Bash。** 虽声明兼容 Windows Git Bash，但当前项目要求 PowerShell 包装、
   F 盘缓存和无 C 盘输出；不能原样安装。
5. **很多门禁仍是文档与人工判断。** 它能改善治理，但不能替代 Godot 运行状态、输入轨迹、
   截图新鲜度和诊断关联。
6. **上游未提供可验证示例游戏闭环。** 因此其收益更多是流程完整性，不是已经证明的
   Godot 自动开发成功率。

采用等级：**选择性提炼，不作为依赖。**

## godot-ai 客观评估

### 已验证的结构

本地快照为 3.2.4，声明 Godot 4.5+、推荐 4.7+，包含 118 个 Python 文件、132 个
GDScript 文件和 104 个测试文件。架构为：

```text
Agent client
  -> FastMCP Python server (HTTP / stdio attach)
  -> loopback WebSocket
  -> Godot EditorPlugin
  -> EditorInterface / SceneTree / EngineDebugger
  -> running game helper autoload
```

它支持多会话路由、结构化错误、超时、编辑器 readiness、运行日志、游戏帧截图、输入序列、
内置 GDScript 测试、自定义 MCP 工具和大量编辑器写操作。HTTP 默认绑定 loopback，
WebSocket 保持 loopback-only，并有 Host/Origin/peer 检查与启动 token。

### Runtime Adapter 覆盖矩阵

| GameMaker 操作 | godot-ai 3.2.4 能力 | 覆盖 | 评价 |
| --- | --- | --- | --- |
| `start` | `project_run` + `editor_state` readiness | 较完整 | 可返回 Godot、插件、session 与启动错误；需 adapter 归一化 |
| `stop` | `project_manage(op="stop")` | 完整 | 幂等，并处理 readiness 同步 |
| `pause` | 无对外游戏暂停操作 | 缺失 | 代码中的 `pause_processing` 是传输内部机制，不是游戏控制 API |
| `resume` | 无对外游戏恢复操作 | 缺失 | 调试器 break 只能停止或人工恢复 |
| `input` | key、mouse、gamepad、action、frame-timed sequence | 较完整 | `input_sequence` 最多 256 steps / 600 frames，适合可回放轨迹 |
| `step` | `input_sequence` 可等待指定帧 | 部分 | 不能先冻结再精确推进 physics/render N 帧 |
| `step_until` | 无条件推进 API | 缺失 | 需要 provider 扩展或 adapter 轮询，且必须有上限 |
| `observe` | runtime scene tree、node info、UI elements、custom tools | 部分 | 原始 SceneTree/属性不是 GameMaker 允许列表语义；应使用项目自定义观察工具 |
| `capture` | `editor_screenshot(source="game")` | 较完整 | 依赖 game helper autoload 和 `project_run`；可报告 stale frame |
| `diagnostics` | `logs_read`、editor errors、game logs、performance | 较完整 | 有 cursor/run_id，适合证据关联；仍需统一错误类别 |
| 白盒测试 | `test_run` + 项目 `res://tests/` | 补充能力 | 适合单元/场景测试，不代替真实输入黑盒验证 |

### 关键优势

1. **与当前 Godot 4.7.2 基线匹配。** Aoye-3 fork main 与 hi-godot 上游 main 指向同一
   revision，降低 fork 漂移不确定性。
2. **运行输入比旧调研快照更成熟。** `input_sequence` 使用帧而不是毫秒安排 action，
   比多次网络调用更适合连招、移动到触发区等测试。
3. **截图和日志有会话语义。** game screenshot 报告 stale frame，日志用 run_id/cursor
   区分不同运行，能支持 Evidence Bundle 新鲜度检查。
4. **允许项目扩展自定义工具。** 项目侧可注册只读 `gamemaker_observe`，集中实现
   `gamemaker_watch` + `_gamemaker_state()` 的有界观察，而不是暴露整个 SceneTree。
5. **编辑能力广。** 对复杂动画、TileMap、资源、信号、UI 等 Godot 序列化操作有价值。

### 风险与约束

1. **没有完整确定性控制。** pause/resume/step/step_until 是当前契约的实质缺口；
   frame-timed input 不能等同于冻结和单步。
2. **默认工具面过宽。** 包含脚本、文件系统、场景写入、`game_eval` 等高权限能力。
   `--exclude-domains` 只能按域裁剪；例如保留 screenshot/logs 所在 editor 域时，也会保留
   `game_eval`。仅靠 Prompt 不足以形成安全边界。
3. **会修改项目。** game capture 依赖 `_mcp_game_helper` autoload，插件会将其写入并保存到
   `project.godot`。这属于需审查、固定版本和可卸载的项目依赖，不是零侵入控制面。
4. **headless 默认不启用插件。** 有意的 CI/headless MCP 需要
   `GODOT_AI_ALLOW_HEADLESS=1`，必须在 F 盘项目包装器中显式管理和验证。
5. **截图仍可能受窗口状态影响。** 后台或最小化窗口可返回 stale frame，不能单独作为 PASS。
6. **遥测默认开启。** 虽声明不采集代码/场景/文件名并可禁用，GameMaker 的可复现与最小
   网络策略应在实测环境默认设置 `GODOT_AI_DISABLE_TELEMETRY=true`。
7. **上游接口仍快速变化。** 必须固定版本，adapter 契约测试通过后才能升级。

采用等级：**进入同场景实测候选；在缺口关闭前不直接晋升为唯一 Runtime provider。**

## 推荐结合架构

```text
Human intent / project decision
          |
          v
GameMaker Production Bridge
  - project semantic query
  - Production Card / Asset Spec
  - Godot Binding / acceptance
          |
          +-------------------------+
          |                         |
          v                         v
Asset Provider              GameMaker Delivery Loop
  -> normalized artifact      -> Maker / Player / Reviewer
          |                         |
          +------------+------------+
                       v
             Authoring / Runtime Adapter
                       |
                       v
              godot-ai 3.2.4 candidate
                       |
                       v
                Godot editor + game
```

关键规则：

- 普通 `.gd`、`.tscn`、配置和文档仍优先使用本地文件编辑与 Git diff。
- godot-ai 只负责 Godot 特有的导入、复杂序列化、运行控制、输入、观察、截图和诊断。
- Agent 角色只知道 GameMaker 操作，不知道上游 MCP 工具名。
- 原始 godot-ai MCP 不直接暴露给普通 Maker、Player 或 Reviewer；由 adapter 进程或受限
  调用层只开放批准的 provider 映射，防止绕过 `game_eval`/文件系统权限。
- TapTapGameJam 中先实现项目候选 adapter/custom observer；通过 Promotion Manifest 后，
  才把去项目化实现提升到 GameMakerAgent。

## 实际开发时的作用逻辑

### 1. 需求与任务形成

用户需要讨论时先显式调用 Studio Advisor；只有经用户确认的决定才交给 Orchestrator。
Orchestrator 再生成最小 task contract：用户可见结果、边界、验收断言、人工检查项。Game
Studios 的专业提问、上下文聚焦和人工确认可作为参考，不采用阶段检测或七阶段目录。

### 2. 计划与实现

只有涉及架构或跨系统风险时才启用 Architect/Designer；默认 Maker 直接实现最小纵切片。
Maker 修改 `game/` 原生 Godot 文件。复杂 TileMap、Animation、资源或编辑器状态可经 adapter
调用 godot-ai，但所有修改必须落到可审查的项目 diff。

### 3. 白盒预检

先运行 Godot CLI smoke 或 godot-ai `test_run`，捕获解析错误、场景加载错误和项目测试。
白盒通过只说明实现可运行，不代表玩法断言成立。

### 4. 黑盒运行验证

Player 通过 GameMaker Runtime Adapter：

1. `start` 启动指定场景并记录 session、Godot/provider/revision；
2. `input` 发送规范化 action 或 frame-timed sequence；
3. `observe` 调用项目只读 `gamemaker_observe`，只返回允许列表字段；
4. `capture` 只在决定性时刻截图，并检查 stale frame；
5. `diagnostics` 拉取同一 run_id/cursor 范围的错误和警告；
6. `stop` 清理运行会话；
7. 生成 Evidence Bundle。

### 5. 独立审核与修复循环

Reviewer 只依据 task contract 和 Evidence Bundle 输出：

- `pass`：断言成立、诊断无阻断、证据新鲜且完整；
- `fail`：运行成功但行为断言失败，或有阻断错误；
- `insufficient_evidence`：截图过期、revision 不匹配、输入轨迹缺失或状态不可关联。

失败返回最小复现给 Maker；Maker 修复后由新的 Player 会话重跑，旧证据不能复用。
玩法手感、乐趣和最终艺术方向继续由人类决定。

### 6. 能力晋升

项目中产生的 adapter 补丁、observer、debug recipe 或测试夹具先留在 TapTapGameJam。
只有项目实测、独立 Reviewer、人工批准、许可证检查、去项目化和 GameMaker 契约测试全部通过，
才进入 GameMakerAgent。

## 建议的最小试点

### 试点 A：godot-ai provider 基线

在 TapTapGameJam 现有 `runtime_probe` 上固定 godot-ai 3.2.4，完成：

1. 启动、输入 `verify_trigger`、读取前后状态、截图、读取日志、停止；
2. 同一输入轨迹连续执行两次，比较状态和证据一致性；
3. 人为制造脚本错误，确认 Reviewer 得到 `fail` 而不是误判为干净运行；
4. 记录 `project.godot` autoload 变化、进程残留、端口、缓存和卸载行为；
5. 默认 loopback、禁用遥测、所有缓存继续留在 F 盘项目目录；
6. 与现有 `satelliteoflove/godot-mcp`、`Erodenn/godot-mcp-runtime` 使用同一矩阵比较。

### 试点 B：有界观察扩展

项目侧实现只读 custom tool：

- 只扫描 `gamemaker_watch` Group；
- 只调用 `_gamemaker_state()`；
- 限制节点数、字段数、字符串长度和总字节数；
- 返回 contract version、session/run/frame 定位；
- 不允许任意路径、任意方法调用或 SceneTree 全量转储。

### 试点 C：轻量顾问与 Agent 增强层

不采用项目阶段检测 router。先在项目 `.vibegame/candidates/gamemaker-agent/` 中重写两个
最小候选：

1. 单入口 Studio Advisor，按需提供玩法、体验、范围和试玩复盘视角；
2. confirmed decision -> task contract -> implementation -> evidence -> review 的最小交接语义。

顾问只在用户明确讨论或复盘时启用，不进入普通开发上下文。候选必须跨 Claude/Codex、
跨宿主、跨 Windows/Linux，不复制 `.claude/` 目录、固定团队拓扑和硬编码模型 ID。首版以
Godot 为明确验证环境，但上层制品不出现具体 MCP 工具名。通过真实
Godot 纵切片验证后，再去项目化晋升到 GameMakerAgent。

## 决策门禁

godot-ai 只有在以下条件同时满足时才建议成为首选 provider：

- runtime probe 两次重放产生等价状态和可关联证据；
- adapter 能物理限制高权限工具，而不只是提示 Agent 不要调用；
- pause/step 缺口有已验证补充方案，或首个里程碑明确不依赖这些能力；
- headless、截图、错误捕获、停止清理和项目污染均通过 Windows/F 盘实测；
- 固定版本的契约测试与升级策略已记录。

如果这些条件失败，godot-ai 仍可保留为**编辑器 authoring provider**，运行验证继续使用
更聚焦、确定性更强的 MCP 或 Godot CLI/测试组合。

## 未决事项

1. `Aoye-3/Claude-Code-Game-Studio` 是私有仓库、已删除仓库，还是 URL 名称错误？
2. 第一里程碑是否真正需要 pause/physics-step，还是 frame-timed input 已足够？
3. 原始 godot-ai 工具是否能完全隐藏在 GameMaker adapter 后，而不注册给工作 Agent？
4. `_mcp_game_helper` autoload 作为项目依赖是否可接受，如何验证卸载后无残留？
5. 项目只读 observer 使用 custom tool addon，还是独立的项目运行桥更安全？
