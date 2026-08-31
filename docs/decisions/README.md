# 架构决策记录

状态流转：`Proposed -> Accepted -> Superseded / Deprecated`。

已接受的 ADR 不删除。新决策改变旧决策时，新增 ADR 并在两份记录中互相链接。

| ADR | 状态 | 决策 |
| --- | --- | --- |
| [ADR-001](ADR-001-separate-framework-and-project-repositories.md) | Accepted | 框架与具体游戏保持独立仓库，通过验证晋升连接 |
| [ADR-002](ADR-002-native-godot-project-and-replaceable-control-adapter.md) | Accepted | 原生 Godot 项目是真实源，MCP 位于可替换控制适配层 |
