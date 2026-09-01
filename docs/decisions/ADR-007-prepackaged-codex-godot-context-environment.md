# ADR-007：GameMakerAgent 是预打包的 Codex + Godot 游戏开发语境环境

## 状态

Accepted

## 日期

2026-09-01

## 背景

成熟的 Codex、Godot 和 Godot MCP 已经能够执行代码、场景、资源、运行、输入、截图和日志
操作。GameMakerAgent 不需要重新实现这些工具。实际缺口位于工具之间：Codex + MCP 缺少游戏
策划与技术美术语境；独立 Skill 的建议难以稳定映射到代码；素材生成结果也没有与 Godot 的
尺寸、帧、Pivot、碰撞、导入和代码引用形成统一交接。

如果 GameMakerAgent 自己实现 Agent Runtime、完整 MCP 或创作前端，会与成熟产品重复，且把
精力从上述语境断点转移到工具基础设施。反过来，如果只发布若干 Markdown Skill，策划决定、
素材规格、Godot 实现和运行证据仍然彼此割裂。

## 决策

GameMakerAgent V1 定位为一个**预打包的 Codex + Godot 游戏开发语境环境**：

- Codex 是唯一 Agent Runtime 和编排者；
- 三个 GameMaker Skill 提供策划、交付和证据审核语境；
- Python Context Core 只负责查询、Schema 校验、跨制品引用、上下文裁剪、记录与确定性检查；
- 成熟 Asset Provider 负责素材生产；
- godot-ai 等成熟 Godot MCP 位于可替换 Adapter 后，负责原生项目操作；
- 原生 Godot 场景、脚本和 Resource 是实现真实源；
- 项目 `.vibegame/gamemaker/` 保存已确认决定和执行结果；
- Godot Dock 只读展示这些结构化记录，不承担聊天、生成、编辑或运行控制。

公共交接链固定为：

```text
Decision Card
  -> Project Semantic Model
  -> Production Card
  -> Asset Spec -> Normalized Asset
  -> Godot Binding
  -> Implementation Record
  -> Evidence Bundle
```

公共制品不出现具体 MCP 工具名。Skill 不把泛泛建议当作完成；图片、代码或工具调用只有在上述
引用链闭合并具有当前 source revision 的证据后才算交付。

项目由用户通过原生 Godot Project Manager 创建一次。GameMaker 从已有、可打开的原生 Godot
项目开始协作，不自动操作 Project Manager，也不承诺无人值守创建项目。

## 交付形态

仓库内可安装包由 repo-scoped Codex Plugin、三个 Skill、Python Context Core、JSON Schema、
Provider capability profile、只读 Godot Dock、去项目化 Fixture 和回归入口组成。第三方 Runtime、
Godot、Godot MCP 和生成模型不被复制或打包。

V1 只声明 Windows、Godot 4.7.2、Python 3.11+、2D 和 GDScript 的已验证组合。首个端到端
纵切片是单场景俯视移动收集，并使用一张 Fixture 专属的 64×64 RGBA 角色精灵。

## 备选方案

### 只发布游戏开发 Skills

实现最少，但 Skill 输出仍无法确定性地约束素材、代码、Godot Binding 和证据，拒绝。

### 自研完整 Agent Runtime 或 Godot MCP

可以统一所有调用，但重复 Codex 与成熟 Godot MCP 的能力，扩大权限、安全、兼容和维护面，拒绝。

### 建设可写 Godot 创作 Dock

体验更集中，但会形成第二个编排和编辑入口。V1 只保留读取结构化开发记录的状态面板，拒绝
写操作。

### 保存完整 Agent 对话作为项目记忆

信息最全，但噪声、隐私和上下文成本不可控。只保存确认摘要、规格、实现结果和证据，拒绝
完整对话归档。

## 后果

- GameMaker 的价值由“是否减少策划缺位、上下文丢失、素材/代码错位和无证据完成”衡量，
  而不是 Agent、Skill 或 MCP 工具数量。
- Python Core 必须保持确定性和工具中立，不能演变为第二套编排器。
- Provider 可以替换，但替换必须通过相同 capability 与 conformance matrix。
- `.vibegame/gamemaker/` 是轻量生产记录，不复制完整 SceneTree，也不取代 Godot 原生文件。
- 新 UI、3D、C#、多引擎、自动项目创建和公共市场发布均需要新的证据与决策。

## 与既有决策的关系

本 ADR 细化 ADR-002 至 ADR-006，不取代原生 Godot 真实源、Provider 可替换、项目孵化、
Production Bridge 或三层验证门禁。若既有计划仍写有“由 godot-ai 自动创建项目”，以本 ADR 的
“用户通过原生 Godot 创建，GameMaker 从已有项目开始”决策为准，并在后续计划同步中修正。
