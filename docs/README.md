# GameMakerAgent 框架技术文档

这里是 GameMakerAgent 可迁移开发框架的唯一技术文档入口。文档解释框架如何
编排 Agent、适配游戏引擎、验证运行结果，以及如何从具体项目中晋升可复用能力。

## 文档地图

### 架构

- [框架与项目仓库边界](architecture/repository-boundaries.md)

### 契约

- [契约索引](contracts/README.md)
- [Runtime Adapter](contracts/runtime-adapter.md)
- [Evidence Bundle](contracts/evidence-bundle.md)
- [Promotion Manifest](contracts/promotion-manifest.md)

### 架构决策

- [ADR 索引](decisions/README.md)
- [ADR-001：框架仓库与游戏项目仓库保持独立](decisions/ADR-001-separate-framework-and-project-repositories.md)
- [ADR-002：原生 Godot 项目是真实源，MCP 位于可替换控制适配层](decisions/ADR-002-native-godot-project-and-replaceable-control-adapter.md)

### 实施计划

- [GameMaker 框架演进计划](plans/framework-evolution-plan.md)

### 调研

- [相似开源项目与采用建议](research/open-source-landscape.md)

## 两套 Doc 的边界

| 文档体系 | 位置 | 允许内容 |
| --- | --- | --- |
| 开发框架 Doc | `GameMakerAgent/docs/` | 架构、契约、适配器、验证、晋升、通用模块 |
| Godot Project Doc | `TapTapGameJam/docs/project/` | GDD、玩法、关卡、资产、项目 ADR、里程碑、复盘 |

如果一份文档同时包含框架规则和游戏设计，必须拆成两份，并用仓库链接建立关系，
不能为了方便把两个上下文重新混在一起。

## 事实来源优先级

发生冲突时，按以下顺序判断框架当前行为：

1. 可执行代码、Schema 和实测运行行为。
2. `docs/contracts/` 中已接受并有验证覆盖的契约。
3. `docs/architecture/` 中的当前架构。
4. 已接受 ADR。
5. 活跃 Plan。
6. 调研报告、共享对话和历史 VibeGame 文档。

低优先级资料仍可提供设计意图，但不能覆盖已经验证的事实。

## 维护规则

- 新文档必须从本索引或下级索引可达。
- 架构文档只描述已落地事实；未来工作进入 Plan。
- ADR 不删除；决策变化时新增 ADR 并标记取代关系。
- 调研必须记录来源、查询日期、许可证和未经本地验证的风险。
- Plan 中每项任务都要包含验收标准、验证方式和依赖。
- 项目候选能力未通过 Promotion Gate 前，不得写成框架已经具备的能力。
