# ADR-005：GameJam 开始前先在框架本地 Lab 搭建并测试通用底座

## 状态

Accepted

## 日期

2026-09-01

## 背景

ADR-003 选择先在具体游戏项目中孵化能力，再晋升到 GameMakerAgent。这适合来自真实玩法的
Skill、Adapter 和验证经验，但当前 GameJam 将于 2026-10-01 开始。如果所有通用底座都等待
届时再开发，会把框架风险、Provider 风险和游戏制作风险集中到同一阶段。

本地已经存在 VibeGame 生产语义、Studio Advisor 候选、Godot Runtime Probe、godot-ai 和
GameStudio 研究快照。把这些仓库整份复制进 GameMakerAgent 会产生双份 Git 历史、许可证
混杂、同步负担和具体游戏污染；完全不迁入任何可执行制品，又无法在 GameJam 前建立回归基线。

## 决策

1. 在 GameMakerAgent 中建立 `lab/`，用于 GameJam 前的通用框架开发和测试。
2. Lab 可以接收经过选择、去项目化并记录来源的最小制品，例如 Studio Advisor 候选、Godot
   Runtime Probe、契约示例和 Provider conformance fixture。
3. 不复制或 vendor 完整 VibeGame、TapTapGameJam、godot-ai、GameStudio 仓库。外部 Provider
   通过固定 revision、安装说明或 Adapter 接入。
4. 本地 Godot 编辑器可以复制到 `.tools/`，但必须被 Git 忽略，并通过 `_sc_` self-contained
   模式把编辑器数据、设置和缓存限制在当前 F 盘工作区。
5. Lab 测试通过只代表通用合同和技术路径成立，不代表真实游戏价值已经验证。
6. 来自玩法、关卡、资产生产或玩家体验的能力，在进入稳定目录前仍必须接受真实 Godot 内容
   纵切片验证和人工 Promotion Gate。
7. Stable `skills/`、`adapters/`、`contracts/` 和 `evals/` 仍只接收通过门禁的去项目化制品；
   未通过门禁的实现留在 `lab/`。

## 与既有决策的关系

本 ADR 部分修订 ADR-003 的**时间顺序**，不取消项目验证：通用底座可先在框架 Lab 开发，
项目衍生能力仍先在项目产生；两类能力最终都必须通过真实项目纵切片才能成为稳定框架能力。

## 备选方案

### 整仓复制所有本地项目

可以立即获得大量文件，但会复制 Git 仓库和游戏资产，并使 GameMaker 难以区分依赖、参考和
自身实现，拒绝。

### 等待 GameJam 开始后再开发框架

能够直接使用真实需求，却会让框架调试挤占比赛制作窗口，拒绝。

### 现在直接把候选放入稳定目录

目录更简单，但会把尚未经过真实使用的能力伪装成已发布合同，拒绝。

## 后果

- GameMakerAgent 可以立即进行契约、Godot 夹具和 Provider 测试。
- `lab/` 成为明确的实验边界，后续必须主动晋升，不能被稳定代码隐式依赖。
- 框架开发与 GameJam 制作时间解耦，但最终产品价值仍要由真实游戏验证。
- 所有迁入制品都需要来源、许可证、revision 和改写记录。
