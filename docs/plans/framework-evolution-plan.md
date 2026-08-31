# 实施计划：GameMaker 项目驱动框架演进

## 状态

Active

## 目标

以 TapTapGameJam 的获奖导向制作过程为真实验证场，逐步把 VibeGame 中已经有效的
Agent 编排、运行控制、证据审查和 Self-Evolve 能力提炼为独立 GameMakerAgent
框架。框架工作必须缩短项目交付路径，不能为了抽象完整而阻塞游戏制作。

## 成功标准

- TapTapGameJam 始终是可直接由 Godot 打开的原生项目。
- Player 和 Reviewer 能依据可回放输入、结构化状态、截图和诊断形成闭环。
- 项目能力只有通过 Promotion Gate 后才成为 GameMaker 的稳定资产。
- GameMaker 不依赖 TapTapGameJam 的路径、玩法、资产或私有状态。
- 两套 Doc 分别保持可导航、无职责混写，并与实际实现同步。

## 已接受的架构决策

- [ADR-001](../decisions/ADR-001-separate-framework-and-project-repositories.md)：双仓独立、项目驱动晋升。
- [ADR-002](../decisions/ADR-002-native-godot-project-and-replaceable-control-adapter.md)：原生 Godot 项目与可替换 Runtime Adapter。

## 依赖关系

```text
双仓和 Doc 边界
  -> Runtime / Evidence / Promotion 契约
    -> 项目验证场景与 MCP 实测
      -> VibeGame 最小纵切片提炼
        -> TapTapGameJam 真实功能闭环
          -> 可复用能力晋升
            -> 资产契约、回归基准与安全加固
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

## Phase 1：Godot 运行验证基线

### Task 1.1：确定 Godot 技术基线

**状态：** In progress

**验收标准：**

- [ ] 项目接受 Godot 稳定版本和 GDScript/C# 范围的 ADR。
- [x] Godot 4.7.2 CLI 已在当前工作区完成导入和无窗口运行。
- [x] 候选决策已进入 TapTapGameJam 项目 ADR；框架只记录兼容范围。

**验证：** 从项目仓库执行一次无人工编辑器操作的干净启动。

**依赖：** Checkpoint 0。

### Task 1.2：制作项目内最小验证场景

**状态：** In progress

**验收标准：**

- [x] `verify_trigger` 使 `verification_value` 从 0 变为 10。
- [x] 场景通过 `gamemaker_watch` 和 `_gamemaker_state()` 暴露有界状态。
- [ ] 场景包含一个通过和一个故意失败的验证用例。

**验证：** Godot 原生测试或 CLI smoke 能复现预期状态变化。

**依赖：** Task 1.1。

**所有权：** 场景属于 TapTapGameJam；通用契约属于 GameMakerAgent。

### Task 1.3：同场景实测 Godot MCP 候选

**状态：** Pending

**验收标准：**

- [ ] 至少比较 `satelliteoflove/godot-mcp` 与 `Erodenn/godot-mcp-runtime`。
- [ ] 使用相同的启动、输入、推进、状态、截图、错误和清理矩阵。
- [ ] 记录版本、许可证、安全边界、项目污染和失败模式。

**验证：** 获胜候选从干净项目状态重复两次并产生等价证据。

**依赖：** Task 1.2。

## Checkpoint 1：运行依赖决策

- [ ] 人工确认 Godot 与 MCP 版本。
- [ ] 选中依赖被固定，替换条件被记录。
- [ ] 任意脚本执行、进程和网络权限有明确默认策略。

## Phase 2：提炼 VibeGame 最小纵切片

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

**验证：** 对通过、玩法失败和证据不完整三套夹具运行审核。

**依赖：** Task 2.1。

### Task 2.3：建立最小 Agent 编排

**状态：** Pending

**验收标准：**

- [ ] 首版只保留 Orchestrator、Maker、Player、Reviewer 四个职责阶段。
- [ ] Designer、Artist 或专业 Reviewer 仅在任务需要时启用。
- [ ] 每阶段输入、输出、失败回退和人工门禁有契约。

**验证：** 使用验证场景完成一次发现失败、修复、复验的闭环。

**依赖：** Task 2.2。

## Checkpoint 2：首个框架闭环

- [ ] 不依赖 TapTapGameJam 私有路径即可运行契约测试。
- [ ] 项目能通过适配器完成一次真实 Godot 闭环。
- [ ] VibeGame 来源、保留语义和有意舍弃行为已记录。

## Phase 3：服务 GameJam 真实制作

每次只选择一个当前游戏功能作为纵切片：规格、实现、运行、证据、审核和修复必须
一起完成。具体功能与获奖策略由 TapTapGameJam 的项目 Plan 决定，不写入本计划。

框架侧每个纵切片只回答两个问题：

1. 现有框架是否让项目更快获得可信结果？
2. 这次产生的能力是否已经通用到值得晋升？

## Phase 4：晋升、资产与回归

### Task 4.1：实现 Promotion Gate

项目候选经过静态检查、项目测试、运行重放、Reviewer、人工审批、去项目化、
许可证检查和框架回归后，才能进入稳定目录。

### Task 4.2：定义 Engine-neutral Asset Contract

以真实资产流水线为输入，定义帧、FPS、Pivot、碰撞提示、导入参数、来源和许可证，
再分别生成 Godot 或其他引擎制品。

### Task 4.3：建立框架回归基准

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
| Agent 角色数量膨胀 | 中 | 首版四阶段；新增角色必须证明质量收益 |

## 当前开放问题

1. TapTapGameJam 首版固定的 Godot 版本是什么？
2. 首版只支持 GDScript，还是必须同时支持 C#？
3. 第一个用于 MCP 对比的项目玩法状态是什么？
4. 项目侧语义状态采用 Group、`_gamemaker_state()`，还是两者结合？

这些问题会改变项目实现，必须在进入 Phase 1 时由项目事实或人工决策确认。
