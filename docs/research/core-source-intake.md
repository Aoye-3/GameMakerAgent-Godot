# 核心竞品源码吸收清单

## 状态与范围

Task 1.0 完成快照，日期 2026-09-01。本报告只回答四个固定源码版本中哪些能力应被
GameMaker **采用（ADOPT）**、**改写后采用（ADAPT）**或**明确拒绝（REJECT）**。
它不创建 Task 1.1 的查询合同，不起草 Task 1.2 的正式 Schema，不安装 godot-ai，也不代表
任何 Provider 已接入。

源码通过当前仓库 Git 对象库中的只读 remote-tracking ref 研究，没有检出外部工作树、复制
仓库或 vendor 上游目录。机器可读来源见
[`lab/sources/upstreams.json`](../../lab/sources/upstreams.json)，迁入边界见
[来源迁入清单](source-intake-manifest.md)。

| 来源 | 固定 ref | Revision | 许可证 | 本次深度 |
| --- | --- | --- | --- | --- |
| VibeGame | `research/vibegame/main` | `7549e57105c6abf1848f714aea63762d540ce04f` | Apache-2.0 | Schema、引擎实现、角色规范与测试规范逐文件阅读 |
| Claude Code Game Studios | `research/claude-code-game-studios/main` | `984023ddac0d5e27624f2baacde6105e45de375f` | MIT，Copyright (c) 2026 Donchitos | Skill、Agent、规则和证据模板逐文件阅读 |
| GameStudio | `research/gamestudio/main` | `6027706e8923ba157a22a546c4c0be4b14b0ef4d` | MIT，Copyright (c) 2026 bullish0x | 与 Game Studios 逐文件 diff，并阅读新增资产/引擎资料 |
| godot-ai | `research/godot-ai/main` | `a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e` | MIT，Copyright (c) 2025 Godot AI contributors | Python MCP 工具注册、工具面文档与许可证阅读；未安装、未运行 |

决策标签含义：

- **ADOPT**：保留语义本身；若未来写入本仓库，仍需使用 GameMaker 命名和自己的测试。
- **ADAPT**：只吸收解决的问题与约束，重新表达为 GameMaker 的 Skill、Contract、Schema、
  检查器、行为用例或 Provider；不复制上游产品结构。
- **REJECT**：明确不进入 V1，避免其以后以默认值、目录或隐式工作流回流。

## VibeGame：保留生产关系，不保留 Phaser 引擎

本节各条均来自 Apache-2.0 源码。没有复制实现代码；若以后复制实质性片段，必须同时保留
Apache-2.0 NOTICE/许可证义务，不能只依赖本报告的语义归纳。

| 决策 | 源文件 / 符号 | 解决的问题 | GameMaker 目标形态 | 必要改写 | 明确拒绝项 | 许可证 |
| --- | --- | --- | --- | --- | --- | --- |
| ADOPT | `src/.vibegame/schema/manifest.schema.json`：`$defs.assetEntry`、稳定 manifest key | 代码、场景和素材文件名漂移；占位素材替换后引用失效 | Asset Spec Schema 的稳定 `asset_id` 与归一化制品引用；行为用例 `SRC-03` | 使用 Provider-neutral 标识和 Godot `res://` 绑定；补来源、许可、透明度和归一化状态 | VibeGame 的 manifest 文件布局、placeholder 类型和 tileset 运行模型 | Apache-2.0 |
| ADAPT | 同一 Schema 的 `frameWidth`、`frameHeight`、`sprites[].bbox/pivot`；`src/.vibegame/spec/engine/animation-guide.md` 的 Pivot cascade；`AnimationPlayer._applyCurrentFrame()` | 帧裁切、尺寸变化和锚点漂移导致角色浮空或动画抖动 | Asset Spec 候选字段 + Godot Binding 的 `SpriteFrames` / Animation / transform 验证点；检查器 | 将 Phaser origin/pivot 层级翻译成 Godot 节点、AtlasTexture/region 和资源导入事实；默认值由项目语义查询，不照抄 `[0.5, 1]` | Phaser `setOrigin`、全局 animation key 和自定义 AnimationPlayer 实现 | Apache-2.0 |
| ADAPT | `src/.vibegame/spec/engine/collision-guide.md`：`ColliderDef`、visual/collider pivot 关系 | 画面脚底、碰撞体和攻击/触发范围无法对齐 | Godot Binding 的 shape、层/掩码、offset、visual-alignment 与 debug-capture 验证点 | 使用 Godot `CollisionShape2D/3D`、资源和世界单位；碰撞尺寸不得从图片像素静默推断 | Arcade Physics body、axis-aligned 限制和 VibeGame collider Schema | Apache-2.0 |
| ADAPT | `project.schema.json` 的入口、manifest、inputMap；`scene.schema.json/$defs.nodeDef` 的 visual/script/config/collider/animation 关系 | Agent 缺少“入口—输入—场景—素材—行为”的最小项目语义 | Project Semantic Model 查询字段和 Production Card 的复用/新增关系 | 只返回任务所需事实和 revision；Godot `.godot/.tscn/.tres` 保持真实源 | 复制完整 SceneTree、建立平行 Scene/Node JSON，或把 `scaleMode` 等 Phaser 设置写入公共合同 | Apache-2.0 |
| ADAPT | `RuntimeController.activate/continue/pause/play/snapshot()`；`RuntimeBridge._cmdInput/_cmdClick/_cmdDrag/_cmdKey/_cmdConsoleGet/_cmdNetworkGet()` | 输入、推进、观察和诊断分散，无法形成可重放运行会话 | Runtime Adapter Contract、假 Provider 与 conformance 行为用例 | 归一化生命周期、action 输入、有限推进、观察、截图、日志、超时和错误；Provider 自报不支持能力 | RuntimeBridge/WebSocket/DOM 事件实现、任意 eval、Phaser Runtime 外壳 | Apache-2.0 |
| ADAPT | `src/agents/player.md`、`src/agents/reviewer.md`、`src/.vibegame/spec/test/index.md` | “测试通过”混淆了状态、画面、手感和证据新鲜度 | Evidence Bundle / Evidence Reviewer 检查器；`SRC-04` | 同一 run 关联输入、结构化状态、截图、诊断、Provider 和 source revision；视觉、状态和人工手感分别裁决 | 固定 Player/Reviewer 子 Agent 数量、任务目录模板和 VibeGame CLI 命令 | Apache-2.0 |

VibeGame 的总体拒绝项是 `src/engine/` Phaser 外壳、Scene/Node 平行数据模型、全局阶段/任务状态机、
Hook 驱动的固定角色链和完整 self-evolve 机制。GameMaker 只保留跨引擎仍成立的关系与行为用例。

## Claude Code Game Studios：把专业提问压缩为字段、检查器和顾问参考

本节各条来自 MIT 源码。目标是提炼知识，不复制 `.claude/` 产品目录、模板正文或角色提示。

| 决策 | 源文件 / 符号 | 解决的问题 | GameMaker 目标形态 | 必要改写 | 明确拒绝项 | 许可证 |
| --- | --- | --- | --- | --- | --- | --- |
| ADAPT | `.claude/skills/asset-spec/SKILL.md`：Phase 2–5、Asset ID Assignment、Shared Asset Protocol | 资产遗漏、重复生产、视觉要求与技术限制脱节 | Asset Spec 候选字段；资产复用检查器；`SRC-02`、`SRC-03` | 保留职责、视觉约束、尺寸/帧、格式、命名、预算、来源/许可、复用、归一化和验收；生成提示仅作 Provider 可选输入 | 强制先有 GDD/Art Bible、逐阶段问答、Markdown manifest、每次并行生成两个 Agent | MIT |
| ADAPT | `.claude/agents/technical-artist.md` | 艺术输出在格式、导入、性能和引擎约束上不可用 | Asset Spec 技术字段 + 按需 technical-art 顾问参考 | 只在存在真实视觉/性能取舍时加载；引擎约束由 Godot Binding 与项目语义提供 | 常驻 Technical Artist Agent、未经项目预算支持的固定数值 | MIT |
| ADAPT | `.claude/skills/asset-audit/SKILL.md`：Phase 3 | 文件存在不代表命名、尺寸、格式、引用和预算合规 | 只读 Asset checker | 项目规则驱动；分别输出 blocking/advisory；增加透明度、帧布局、pivot/trim、来源许可和 Godot import/binding 检查 | 把 power-of-two、PNG/OGG 或目录模式设为跨项目硬规则；自动删除 orphan | MIT |
| ADAPT | `.claude/skills/scope-check/SKILL.md`：baseline comparison、Cut/Defer/Keep/Flag | 新需求不断加入而未说明取舍，核心玩家结果被稀释 | `studio-advisor` 的按需 scope 参考 | 比较已确认基线，优先保留玩家承诺、最大风险和最便宜验证；无基线则先请求确认 | 用“增加 10%/25%/50%”自动裁决 PASS/FAIL，或建立持续阶段状态机 | MIT |
| ADAPT | `.claude/skills/playtest-report/SKILL.md`：结构化发现与 design-intent 对照 | 观察、解释、Bug 和设计建议混写，复盘无法行动 | `studio-advisor` 的按需 playtest 参考 | 分离 observation、hypothesis、confidence、priority、next experiment；人工决定体验质量 | Director Gate、完整报告模板和用文档投票代替玩家证据 | MIT |
| ADAPT | `.claude/skills/test-evidence-review/SKILL.md` §§5–6；`.claude/docs/templates/test-evidence.md` | 有测试文件或截图但验收项未覆盖、附件缺失或证据过期 | Evidence Reviewer 检查器 + `SRC-04` | 以 acceptance claim、artifact existence、run/revision freshness 和诊断完整性给出 PASS/FAIL/INSUFFICIENT_EVIDENCE | 固定三角色签字、以每函数断言数判断质量、沿用 ADEQUATE/INCOMPLETE/MISSING 作为公共 verdict | MIT |

## GameStudio：只接收增量，不重复接收共同知识

GameStudio 固定版本包含 55 个 Agent，并在 README 中声明 182 个 Skill。它的 canonical
`.agents/` 与多宿主镜像是一个完整产品结构，不是 GameMaker V1 的目标。以下判断独立遵守
GameStudio 的 MIT 许可证；内容相似不等于许可证或著作权归属可以合并处理。

### 与 Claude Code Game Studios 的逐文件去重

下表使用 Git blob-to-blob diff 比较固定 refs。差异数字是新增/删除行；大部分变化只是
`.claude` 改为 `.agents` 或移除 `model:` 字段。

| 知识组 | 固定源码 diff 证据 | 单一吸收入口 | 结论 |
| --- | --- | --- | --- |
| Asset Spec | `asset-spec/SKILL.md`：`1/2`，仅移除模型字段并改 technical-preferences 路径 | 上一节的 Asset Spec 字段 | GameStudio 不再生成第二套 Skill 或 Schema |
| Asset Audit | `asset-audit/SKILL.md`：`2/3`，仅移除模型字段并将 CLAUDE.md 改为 AGENTS.md | 上一节的只读检查器 | 共用一组规则来源；两份 MIT 来源都保留在 provenance |
| Technical Artist | `technical-artist.md`：`0/1`，仅移除模型字段 | 上一节的技术字段/按需参考 | 不创建第二个顾问角色 |
| Scope | `scope-check/SKILL.md`：`0/1`，仅移除模型字段 | `studio-advisor` scope reference | 不接受第二套阶段或 verdict |
| Evidence Review | `test-evidence-review/SKILL.md`：`0/1`，仅移除模型字段 | Evidence Reviewer checker | 不接受第二套证据模板 |
| Game Designer | `game-designer.md`：`0/1`，仅移除模型字段 | 已有 Studio Advisor lenses | 不扩展为常驻 Game Designer Agent |

### GameStudio 独有增量

| 决策 | 源文件 / 符号 | 解决的问题 | GameMaker 目标形态 | 必要改写 | 明确拒绝项 | 许可证 |
| --- | --- | --- | --- | --- | --- | --- |
| ADAPT | `.agents/agents/web2d-asset-pipeline.md`：Core Practices | atlas 裁切后 pivot/trim 丢失、文件路径耦合、纹理内存失控 | Asset Spec 的 stable key、trim/pivot metadata、compression/mipmap rationale、budget 字段；检查器 | 这些字段只在素材类型与目标 Godot 导入路径需要时出现；预算来自项目事实 | Pixi/Phaser loader、Spine/DragonBones runtime、KTX2/POT 作为默认要求 | MIT |
| ADAPT | `.agents/hooks/validate-assets.sh`：naming warning、JSON blocking；`.agents/docs/hooks-reference/post-merge-asset-validation.md` | 低成本规则不能在交付前稳定重复 | 跨平台、显式调用的 Asset checker 行为用例 | 命名为 advisory；无效结构为 blocking；格式/预算读取项目配置，不硬编码 | 安装 Bash Hook、merge 时自动改项目、固定 4 MB/512 KB/10 MB 阈值 | MIT |
| REJECT | `.agents/adapter-manifest.json` 与 `.claude/.codex/.cursor` 镜像 | 同一大目录适配多个 Agent 宿主 | 无 V1 目标制品 | GameMaker 的合同本身保持宿主中立，必要时再做薄适配 | 复制 canonical Agent/Skill 树或维护多份镜像 | MIT |
| REJECT | `.agents/skills/collision-system`、`input-system`、`camera-system`；Phaser/Pixi/Three.js Skill 集 | 提供 Web/ECS 引擎实现知识 | 无 V1 目标制品 | Godot 专属事实以后从项目和官方 API 查询；跨引擎只保留需求语义 | TypeScript ECS、Phaser 外壳、多引擎 Skill 目录 | MIT |
| REJECT | `.agents/rules/assets-3d.md` | Web 3D glTF、Draco、KTX2 和 LOD 交付 | V1 不覆盖 3D Asset Spec | 若未来真实 3D 纵切片需要，再从官方 Godot 导入事实重新研究 | 把 Web 3D 规则提前写入 2D/Godot-first V1 | MIT |

## godot-ai：工具面只映射到未来 Adapter，不进入公共语义

godot-ai 本次只做源码映射。没有复制 `plugin/addons/godot_ai/`，没有安装 Python 依赖，
没有启用插件，也没有运行真实 Godot conformance。以下能力仍全部是 **候选 Provider 映射**。

| 决策 | 源文件 / 符号 | 未来 GameMaker 端口 | 映射与缺口 | 明确拒绝项 | 许可证 |
| --- | --- | --- | --- | --- | --- |
| ADAPT | `src/godot_ai/tools/session.py`：`session_activate/list`；`tools/editor.py`：`editor_state` | Authoring/Runtime Provider 的 connect、select、health/readiness | Adapter 保存 provider/session/version；把 importing、playing、live、break 等状态归一化 | 上层制品保存 MCP session/tool 名 | MIT |
| ADAPT | `tools/scene.py`：`scene_open/save/get_hierarchy`、`scene_manage(create/save_as/get_roots)`；`tools/node.py`：get/create/set/find/manage | Authoring Provider 的 scene/node 操作 | 只开放 Godot Binding 所需操作；写后必须落到可审查 `.tscn/.tres` diff | 把 raw SceneTree 复制进 Project Semantic Model | MIT |
| ADAPT | `tools/script.py`：`script_create/patch/attach/manage`；`tools/filesystem.py`：read/write/reimport/scan/search | Authoring Provider 的 script/file/import 操作 | `reimport`、`scan` 与脚本诊断是 Godot 特有语义；Adapter 统一 import pending、parse failure、not found | 普通文本编辑强制经过 MCP；暴露任意文件系统写入给 Reviewer | MIT |
| ADAPT | `tools/resource.py`：`resource_manage(search/load/assign/get_info/create/physics_shape_autofit/...)`；`tools/input_map.py`；`tools/project.py:set_main_scene` | Godot Binding 执行端口 | 支撑 Resource 创建/指派、InputMap 与主场景；特化材质/粒子等只有绑定需要时才授权 | 把 `resource_manage` op 或 godot-ai 名称写入 Asset Spec/Godot Binding | MIT |
| ADOPT | `tools/batch.py:batch_execute()` 的 stop-on-error + rollback 语义 | Authoring Provider 可选 atomic batch capability | 上层只请求原子写意图；Provider 声明哪些子操作可回滚，不能假定所有文件写可撤销 | 将 plugin command 名暴露为公共 batch Schema | MIT |
| ADAPT | `tools/project.py:project_run()`、`project_manage(stop)` | Runtime Provider `start/stop` | 映射 main/current/custom、autosave、liveness、break 和 recent errors；记录 run/session | 把“tool call success”当作游戏已 live 或验收通过 | MIT |
| ADAPT | `tools/game.py:game_manage(input_key/input_mouse/input_gamepad/input_action/input_sequence/input_state)` | Runtime Provider `input` 与有限 `advance` | action 和 frame-timed sequence 可支持重放；但没有冻结后精确单步、pause/resume 或 step_until，必须在 conformance 中标为部分支持 | 用网络调用次数或 `settle_frames` 冒充确定性 physics/render step | MIT |
| ADAPT | `tools/game.py:get_scene_tree/get_node_info/get_ui_elements` | Runtime Provider `observe` 的底层候选 | 默认只调用项目侧有界 observer（`gamemaker_watch` / `_gamemaker_state()`）；raw tree 仅诊断且限额 | 任意路径、任意属性、完整运行 SceneTree 成为公共观察合同 | MIT |
| ADAPT | `tools/editor.py:editor_screenshot/logs_read/editor_state` | Runtime Provider `capture/diagnostics` + Evidence Bundle | 保存 source、run/session、cursor、stale-frame、provider/version 和 source revision；截图与状态必须同一 run 可关联 | 过期截图、无 run_id 日志或单张图片独立给 PASS | MIT |
| ADAPT | `tools/testing.py:test_run/test_manage(results_get)` | 可选白盒预检 | 可补充解析、单元和场景测试；不能替代真实输入、状态和画面证据 | 用 GDScript 测试通过代替玩家结果 | MIT |
| REJECT | `docs/tool-surface.md` 描述的约 43 个 MCP 工具与 `<domain>_manage` 全量面；`editor_manage(game_eval)` | 无公共端口 | Phase 2 只授权理论合同需要的最小子集，并用相同 conformance matrix 比较替代 Provider | 向 Maker/Player/Reviewer 直接暴露全量工具、任意 eval 或插件命令 | MIT |

固定源码还显示一个重要边界：godot-ai 以已连接 EditorPlugin/session 为中心，提供 scene create/open
与 project settings，但没有独立的“在空目录创建并启动一个完整 Godot 项目”公共操作。完整 MVP
的项目创建/打开能力不能在 Task 1.0 中假定已覆盖，必须在 Task 2.2 通过真实安装与 Fixture 实测
确认 Adapter 的组合路径或明确降级。

## 压缩后的单一吸收结果

Task 1.0 不新增正式 Skill、Contract 或 Schema，只冻结后续任务允许使用的知识入口：

| 目标形态 | 允许进入的内容 | 不允许进入的内容 | 首次落地任务 |
| --- | --- | --- | --- |
| `studio-advisor` references | 玩家承诺、范围 Cut/Defer/Keep、playtest observation/hypothesis/next experiment；`SRC-01` | 全阶段路由、固定 Director/Designer 团队、百分比式 scope verdict | Task 1.3；候选已有，真实价值 Phase 3 验证 |
| Project Semantic Model Contract | 任务所需的入口、输入、可复用场景/资源、玩家动词、资产惯例、source revision | 完整 SceneTree、Phaser schema、全量项目文档注入 | Task 1.1 |
| Production Card / Asset Spec / Godot Binding Schema | 稳定 ID、职责、复用、视觉与技术约束、尺寸/帧/透明度/pivot/trim/格式、来源/许可、归一化、Godot import/resource/scene/animation/collision/验收；`SRC-02`、`SRC-03` | 生成器或 MCP 工具名、强制 GDD/Art Bible、未经项目确认的固定预算 | Task 1.2 |
| Asset checker | JSON/Schema、命名、尺寸、透明度、帧布局、pivot/trim、格式、预算、引用、来源许可、Godot import/binding；blocking/advisory 分级；`SRC-02`、`SRC-03` | 删除文件、硬编码 POT/格式/预算、只检查“文件存在” | Task 1.2 后随假 Provider 用例实现 |
| Runtime / Evidence Contract 与检查器 | lifecycle、action/input trace、有限推进、bounded observe、capture、diagnostics、run/session/provider/source revision、staleness；`SRC-04`、`SRC-06` | 工具成功即完成、raw SceneTree、固定 Agent 数量、旧证据复用 | Task 1.4 |
| godot-ai Provider | 上述 Authoring/Runtime 端口的受限映射、能力声明、错误归一化和清理；`SRC-05`、`SRC-06` | 安装即接入、全量工具直通、公共制品出现 godot-ai 名称 | Task 2.2 |

## 后续制品必须反查的行为用例

以下 ID 是本清单的追踪锚点，不是本任务已实现的测试：

| ID | 行为 | 来源结论 | 未来验收 |
| --- | --- | --- | --- |
| `SRC-01` | 普通修错或明确实现请求不加载顾问知识 | 拒绝 CCGS/GameStudio 常驻岗位与阶段路由 | 路由用例证明只加载任务局部语义 |
| `SRC-02` | 新素材缺少尺寸、帧/透明度、pivot、格式、来源或许可时不能进入 Provider | VibeGame 资源关系 + Game Studios Asset Spec/Technical Artist | Schema/检查器返回字段级错误，不让 Agent 临时猜测 |
| `SRC-03` | 原始素材归一化或替换后稳定 ID 不变，Godot Binding 指向新制品且可反查来源 | VibeGame manifest key + GameStudio stable key/trim metadata | 假 Provider 往返与引用检查通过 |
| `SRC-04` | revision、run/session、输入轨迹、状态、截图或诊断缺失/过期时 verdict 为 `INSUFFICIENT_EVIDENCE` | VibeGame Player/Reviewer + CCGS evidence review + godot-ai stale/run metadata | Evidence Reviewer 对完整、失败、过期三组 fixture 正确分类 |
| `SRC-05` | 更换假 Provider 后上层 Production Card、Asset Spec、Binding 与 Evidence 语义不变 | godot-ai 只位于 Adapter 后 | Provider conformance 使用同一行为矩阵 |
| `SRC-06` | Provider 不支持 pause、deterministic step 或 step_until 时显式降级/拒绝，不静默模拟 | VibeGame 完整 runtime semantics 与 godot-ai 当前缺口对照 | capability negotiation 与 bounded failure 用例通过 |

## 复查方法与限制

固定 ref 可用以下只读命令复查：

```powershell
git rev-parse research/vibegame/main
git show research/vibegame/main:src/.vibegame/schema/manifest.schema.json
git diff research/claude-code-game-studios/main:.claude/skills/asset-spec/SKILL.md `
  research/gamestudio/main:.agents/skills/asset-spec/SKILL.md
git show research/godot-ai/main:src/godot_ai/tools/game.py
```

本报告验证的是**固定源码中存在的接口和规则**，不是这些规则在 GameMaker、Godot 4.7.2
或真实游戏制作中的有效性。字段与检查器要在 Task 1.1–1.4 的假 Provider 用例中成立；
godot-ai 的安装方式、权限、项目污染、失败模式和真实能力必须留到 Task 2.2 重复实测。
