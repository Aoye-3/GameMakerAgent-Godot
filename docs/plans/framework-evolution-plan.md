# 实施计划：GameMaker 项目驱动框架演进

## 状态

Active

## 目标

以 TapTapGameJam 的获奖导向制作过程为真实验证场，逐步把 VibeGame 中已经有效的
统一生产语义、Agent 职责、运行控制、证据审查和 Self-Evolve 能力提炼为独立
GameMakerAgent 框架。框架工作必须缩短项目交付路径，不能为了抽象完整而阻塞游戏制作。

## 成功标准

- TapTapGameJam 始终是可直接由 Godot 打开的原生项目。
- Player 和 Reviewer 能依据可回放输入、结构化状态、截图和诊断形成闭环。
- 一次新增内容能从玩家结果进入素材规格、Godot Resource / Scene 绑定和运行证据，且不
  需要 Agent 临时猜测关键导入约束。
- 项目能力只有通过 Promotion Gate 后才成为 GameMaker 的稳定资产。
- GameMaker 不依赖 TapTapGameJam 的路径、玩法、资产或私有状态。
- 两套 Doc 分别保持可导航、无职责混写，并与实际实现同步。

## 已接受的架构决策

- [ADR-001](../decisions/ADR-001-separate-framework-and-project-repositories.md)：双仓独立、项目驱动晋升。
- [ADR-002](../decisions/ADR-002-native-godot-project-and-replaceable-control-adapter.md)：原生 Godot 项目与可替换 Runtime Adapter。
- [ADR-003](../decisions/ADR-003-project-incubated-agent-enhancement-layer.md)：项目 `.vibegame` 孵化 Agent 增强层，验证后晋升。
- [ADR-004](../decisions/ADR-004-production-bridge-and-godot-native-source-of-truth.md)：以 Production Bridge 连接玩法、素材和 Godot 原生实现。

## 依赖关系

```text
已有双仓边界与 Runtime / Evidence / Promotion 契约
  -> 框架本地 Lab + Studio Advisor / Godot Probe 候选
    -> Production Bridge 制品草案
      -> 最小 Delivery Loop 与 Godot Provider 实测
        -> 含新素材的真实关卡/内容纵切片
          -> 检查器、技能和契约按证据晋升到 GameMakerAgent
```

## Phase 0：框架基础

### Task 0.1：建立两套独立 Doc 体系

**状态：** Completed

**验收标准：**

- [x] GameMakerAgent 有框架技术文档入口、维护规则和实施 Plan。
- [x] TapTapGameJam 有独立的 `docs/project/` 项目文档入口。
- [x] 两边都明确禁止框架文档与游戏设计混写。

**验证：** 检查所有入口链接可达，并搜索边界声明。

**依赖：** 无。

### Task 0.2：定义最小框架契约

**状态：** Completed

**验收标准：**

- [x] Runtime Adapter 定义生命周期、输入、推进、观察和诊断语义。
- [x] Evidence Bundle 定义一次可复现验证所需的最小证据。
- [x] Promotion Manifest 定义项目能力晋升的来源、门禁和审批。
- [x] Evidence 与 Promotion 提供可解析的 JSON Schema 草案。

**验证：** Schema 可被 JSON 解析器读取；示例字段与契约文档一致。

**依赖：** Task 0.1。

### Task 0.3：记录开源调研和采用边界

**状态：** Completed

**验收标准：**

- [x] 候选项目按架构、运行时、测试三个类别记录。
- [x] 区分可借鉴模式、可能依赖和不采用内容。
- [x] 未经过本地验证的能力明确标注为待实测。

**验证：** 所有外部结论链接到项目官方仓库或官方规范。

**依赖：** 无。

## Checkpoint 0：基础可执行

- [x] 框架与项目文档边界已写入仓库规则。
- [x] 首批契约和 Plan 可被后续 Agent 直接读取。
- [x] 尚未把候选 MCP 的 README 声明误写成已验证能力。

## Phase 0.5：建立框架 Lab 并验证顾问层

### Task 0.4：实现 Studio Advisor 候选

**状态：** In progress — 候选已迁入框架 Lab，静态用例可解析，等待真实使用验证。

单入口顾问层从项目候选选择性迁入 `lab/candidates/studio-advisor/`，按需提供玩法、体验、
范围和试玩复盘视角。它只讨论和形成用户确认的 Decision Card，不参与普通编码、运行或
自动任务分配。

**验收标准：**

- [ ] 明确讨论请求能调用相关视角，普通实现请求不加载顾问内容。
- [ ] 未确认时不写项目文件；确认后只生成轻量决策卡。
- [ ] 顾问不创建 Agent、GDD、任务、代码或场景。
- [ ] 至少用一个真实玩法讨论和一个试玩复盘验证其价值与噪声。

**验证：** 保存输入、顾问输出、用户确认和后续是否减少返工的项目记录。

**依赖：** Checkpoint 0。

### Task 0.5：建立框架本地 Lab 与 Godot Runtime Probe

**状态：** Completed

**验收标准：**

- [x] `lab/` 明确区分候选、夹具和固定来源，不复制完整外部仓库。
- [x] 本地 Godot 4.7.2 位于 Git 忽略的 `.tools/`，运行数据与缓存留在当前 F 盘工作区。
- [x] 去项目化 Runtime Probe 能验证输入、`gamemaker_watch` 和 `_gamemaker_state()`。
- [x] Studio Advisor Eval 与来源清单以显式 UTF-8 解析。
- [x] 一个命令可以运行全部首批 Lab smoke。

**验证：** `powershell -ExecutionPolicy Bypass -File scripts/test-lab.ps1` 输出
`LAB_TEST_PASS`。

**依赖：** Checkpoint 0、ADR-005。

### Checkpoint 0.5：顾问层可用

- [ ] 用户可以自然语言显式启用顾问，无需进入阶段状态机。
- [ ] Programmer 只接收确认决定，不接收完整讨论上下文。
- [ ] 顾问候选仍属于 Lab，尚未被描述为 GameMakerAgent 稳定能力。

## Phase 1：验证 Production Bridge 的最小语义

本阶段先回答 GameMaker 最关键的问题：Codex 如何从项目事实理解玩法、资产约束和 Godot
使用方式。只做任务局部语义，不搬运 VibeGame 的 Phaser Project/Scene/Node 数据模型。

### Task 1.1：建立 Project Semantic Model 查询草案

**状态：** Pending

**验收标准：**

- [ ] 能按需回答 Godot 版本、目录、输入、场景入口、可复用资源、玩家动词和资产惯例。
- [ ] 所有事实可追踪到原生项目 revision，不复制完整 SceneTree。
- [ ] 普通代码修复只加载相关查询结果，不注入全量项目档案。

**验证：** 用三个不同任务查询并检查结果最小性、来源和过期行为。

**依赖：** Checkpoint 0.5。

### Task 1.2：起草 Production Card、Asset Spec 与 Godot Binding

**状态：** Pending

**验收标准：**

- [ ] Production Card 只包含当前内容的玩家结果、节拍、复用、新素材、绑定和验收。
- [ ] Asset Spec 能表达帧、尺寸、格式、透明度、Pivot、来源、许可和归一化要求。
- [ ] Godot Binding 能映射 Resource、导入选项、场景位置、动画/碰撞和验证点。
- [ ] 制品不出现 imagegen、godot-ai 或其他第三方工具名。

**验证：** 用一个现有资产替换案例和一个新资产案例做纸面走查，识别缺失字段与冗余字段。

**依赖：** Task 1.1。

### Task 1.3：限定技能包和上下文路由

**状态：** Pending

**验收标准：**

- [ ] 首版用户可见能力只规划 `studio-advisor`、`game-delivery`、`evidence-review`。
- [ ] Production Bridge 主要由制品、查询器和检查器承担，不新增长驻 Agent。
- [ ] 清楚请求可以直接交付；只有创意取舍未定时才启用 Advisor。

**验证：** 对讨论、普通修错、新关卡、已有功能复验四类请求检查实际加载内容。

**依赖：** Task 1.2。

## Checkpoint 1：生产语义可交接

- [ ] 顾问确认结果能形成最小 Production Card，不把讨论全文注入实现上下文。
- [ ] 同一资产能从玩法职责追踪到 Godot Binding，反向也能找到来源与验收。
- [ ] VibeGame 保留的关系和有意舍弃的引擎模型已记录。

## Phase 2：最小 Delivery Loop

本阶段提炼任务交接、运行证据和独立审核；不建立固定团队或全局阶段状态机。

### Task 2.1：提炼运行时端口与错误模型

**状态：** Pending

**验收标准：**

- [ ] Agent 只调用 GameMaker Runtime Adapter，不知道 MCP 工具名。
- [ ] 超时、取消、无连接、Godot 错误和适配器错误被统一归一化。
- [ ] Phaser 旧行为被记录为迁移参照，而不是强加给 Godot。

**验证：** 契约测试使用假适配器覆盖成功、失败和超时。

**依赖：** Checkpoint 1。

### Task 2.2：提炼 Player / Reviewer 证据闭环

**状态：** Pending

**验收标准：**

- [ ] Player 产生版本化 Evidence Bundle。
- [ ] Reviewer 能只凭证据判断 PASS、FAIL 或 INSUFFICIENT_EVIDENCE。
- [ ] 过期截图、缺少输入轨迹或源版本不一致会被拒绝。
- [ ] 静态、运行状态、运行视觉和人工手感使用不同 verdict，不合并成伪精确分数。

**验证：** 对通过、玩法失败、视觉失败和证据不完整四套夹具运行审核。

**依赖：** Task 2.1。

### Task 2.3：建立最小职责链

**状态：** Pending

**验收标准：**

- [ ] Orchestrator、Maker、Player、Reviewer 是逻辑职责，不要求始终生成四个 Agent。
- [ ] Designer、Artist 或专业 Reviewer 仅在任务需要时启用。
- [ ] 每个交接只包含任务契约、必要项目语义和当前 revision。

**验证：** 使用验证场景完成一次发现失败、修复、复验的闭环。

**依赖：** Task 2.2。

## Checkpoint 2：Agent 增强层骨架

- [ ] 使用假 Adapter 可以完成成功、失败和证据不足三条职责链演练。
- [ ] 普通实现没有加载顾问或全量资产知识。
- [ ] Evidence 与实现 revision 一致。

## Phase 3：Godot 运行验证与 Provider 适配

### Task 3.1：确定 Godot 技术基线

**状态：** In progress

**验收标准：**

- [ ] 项目接受 Godot 稳定版本和 GDScript/C# 范围的 ADR。
- [x] Godot 4.7.2 CLI 已在当前工作区完成导入和无窗口运行。
- [x] 候选决策已进入 TapTapGameJam 项目 ADR；框架只记录兼容范围。

**验证：** 从项目仓库执行一次无人工编辑器操作的干净启动。

**依赖：** Checkpoint 0。

### Task 3.2：完成项目内最小验证场景

**状态：** In progress

**验收标准：**

- [x] `verify_trigger` 使 `verification_value` 从 0 变为 10。
- [x] 场景通过 `gamemaker_watch` 和 `_gamemaker_state()` 暴露有界状态。
- [ ] 场景包含一个通过和一个故意失败的验证用例。

**验证：** Godot 原生测试或 CLI smoke 能复现预期状态变化。

**依赖：** Task 3.1。

**所有权：** 场景属于 TapTapGameJam；通用契约属于 GameMakerAgent。

### Task 3.3：同场景实测 Godot Provider 候选

**状态：** Pending

**验收标准：**

- [ ] 先实测固定版本的 `hi-godot/godot-ai`；存在阻断缺口时再用同一矩阵比较其他 MCP。
- [ ] 使用相同的启动、输入、推进、状态、截图、错误和清理矩阵。
- [ ] 记录版本、许可证、安全边界、项目污染和失败模式。

**验证：** 获胜候选从干净项目状态重复两次并产生等价证据。

**依赖：** Task 3.2、Checkpoint 2。

### Task 3.4：验证 Asset Provider 到 Godot 的交接

**状态：** Pending

**验收标准：**

- [ ] 至少一个图像生成或编辑 Provider 只接收 Asset Spec 所需字段。
- [ ] 生成结果经过尺寸、透明度、帧/Pivot、命名、来源和许可证检查。
- [ ] 同一 Asset Spec 可以更换 Provider，Godot Binding 不随 Provider 工具名改变。

**验证：** 对同一规格产生或替换两个候选素材，至少一个完成 Godot 导入和场景绑定。

**依赖：** Task 1.2、Task 3.3。

## Checkpoint 3：首个框架闭环

- [ ] 不依赖 TapTapGameJam 私有路径即可运行契约测试。
- [ ] 项目能通过适配器完成一次真实 Godot 闭环。
- [ ] 人工确认 Godot 与 Provider 版本、权限策略和替换条件。

## Phase 4：服务 GameJam 真实制作

每次只选择一个当前游戏功能作为纵切片：规格、实现、运行、证据、审核和修复必须
一起完成。具体功能与获奖策略由 TapTapGameJam 的项目 Plan 决定，不写入本计划。

首个纵切片必须是包含新增或修改素材的关卡/内容任务，以验证完整链路：

```text
Production Card -> Asset Spec -> Provider -> Godot Binding -> Runtime Evidence -> Human Verdict
```

框架侧每个纵切片只回答两个问题：

1. 现有框架是否让项目更快获得可信结果？
2. 这次产生的能力是否已经通用到值得晋升？

## Phase 5：晋升与回归

### Task 5.1：实现 Promotion Gate

项目候选经过静态检查、项目测试、运行重放、Reviewer、人工审批、去项目化、
许可证检查和框架回归后，才能进入稳定目录。

### Task 5.2：晋升 Production Contract

只把真实纵切片证明必要且稳定的 Production Card、Asset Spec 和 Godot Binding 字段晋升为
框架契约。引擎中立部分与 Godot 映射分层，删除项目名、路径、资产和 Provider 工具名。

### Task 5.3：建立框架回归基准

从真实项目缺陷中提取最小可公开重放的测试，参考 GameDevBench 和 GameCraft-Bench
的任务、轨迹和证据思想，但不复制项目专属内容。

## 风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 框架工作挤占 GameJam 制作时间 | 高 | 只做当前项目纵切片必需能力；设人工 Checkpoint |
| MCP 候选不稳定 | 高 | 固定版本、契约隔离、保留 CLI 启动和诊断路径 |
| 项目代码过早进入框架 | 高 | Promotion Manifest + 证据 + 人工批准，缺一不可 |
| 两份文档再次混写 | 中 | 独立入口、仓库规则、跨仓链接而非复制正文 |
| 截图看似正确但状态错误 | 高 | 结构化状态、输入轨迹、信号和诊断与截图联合判定 |
| Agent 角色数量膨胀 | 中 | 保留最小逻辑职责；新增角色必须证明质量收益 |
| Production Model 成为第二套 SceneTree | 高 | 只保存任务增量与可丢弃查询；Godot 始终是真实源 |
| 素材生成成功被误判为内容完成 | 高 | 强制经过归一化、Binding、运行视觉与状态验证 |

## 当前开放问题

1. TapTapGameJam 首版固定的 Godot 版本是什么？
2. 首版只支持 GDScript，还是必须同时支持 C#？
3. 第一个用于 MCP 和 Production Bridge 对比的内容纵切片是什么？
4. 项目侧语义状态采用 Group、`_gamemaker_state()`，还是两者结合？
5. 首版 Asset Spec 只覆盖 2D 图像/动画，还是必须同时覆盖音频或 3D？

这些问题会改变项目实现，必须在对应 Task 开始前由项目事实或人工决策确认。
