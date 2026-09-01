# ADR-006：先建立理论框架，再验证真实 Godot，最后执行使用场景 MVP

## 状态

Accepted

## 日期

2026-09-01

## 背景

GameMakerAgent 同时面对三类尚未完全证明的问题：公共生产语义是否成立、Godot 与 Provider
技术能力是否满足合同、完整用户流程是否真正降低返工。如果三类问题在一个真实游戏项目中同时
验证，失败时难以判断责任属于框架设计、MCP 能力、素材管线还是具体游戏实现。

已有 Framework Lab 和 Godot Runtime Probe 已证明本地 Godot CLI、输入与状态观察的最小
技术路径可运行，但它们没有证明 Production Bridge、技能路由或端到端用户价值。反过来，等待
真实项目再定义所有理论合同，会让具体 MCP 的工具形状和项目偶然结构进入公共框架。

## 决策

V1 按三个严格分离、顺序通过的验证层推进：

### 1. 理论框架

先定义 GameMaker 的最小逻辑系统，并通过 Schema、静态行为用例和假 Adapter 验证内部一致性：

- `studio-advisor`、`game-delivery`、`evidence-review` 三个按需技能包的职责和路由；
- Project Semantic Model 的任务局部查询合同；
- Production Card、Asset Spec、Godot Binding 的 Draft 制品；
- Maker、Runtime、Reviewer 的逻辑职责与 Evidence Bundle；
- Asset、Authoring、Runtime Provider 的可替换端口和统一错误语义。

本层不要求真实 Godot 项目、godot-ai 或图像生成服务。它的完成标准也不是文档数量，而是典型
请求可以在假 Provider 上完成讨论、交接、成功、失败和证据不足的合同演练。

### 2. 真实 Godot 技术验证

理论框架通过后，在去项目化的最小 Godot Fixture 上逐项验证技术假设：

- 固定 Godot 和 godot-ai 版本；
- 验证项目创建或打开、场景和脚本编辑、资源导入、运行、输入、状态、截图、日志和清理；
- 用同一 conformance matrix 判断 godot-ai 是否满足 Authoring / Runtime Adapter；
- 单独验证素材文件经过归一化后成为 Godot Resource 并绑定到场景；
- 记录权限、污染、失败模式和降级路径。

本层验证的是“能否可靠执行”，不讨论玩法质量，也不把若干独立技术 smoke 宣称为用户流程成立。

### 3. 使用场景 MVP

前两层通过后，执行一条完整且可复现的最小用户旅程：

```text
用户讨论小型游戏目标
  -> Studio Advisor 形成确认决定
  -> 查询工作区、Godot 基线与随后创建的项目事实
  -> 形成 Production Card / Asset Spec / Godot Binding
  -> Asset Provider 生成至少一个素材并完成归一化
  -> 通过 godot-ai MCP 创建原生 Godot 项目
  -> 完成可运行代码基础
  -> 把素材导入并绑定到实际场景
  -> 运行、输入、状态、截图和诊断形成 Evidence Bundle
  -> Reviewer 与人类给出结论
```

MVP 必须从用户意图走到可打开、可运行的原生 Godot 项目。图片存在、MCP 调用成功或代码文件
生成都不能单独算完成。

## 门禁与回退

- 未通过理论框架门禁，不开始正式 Provider 适配；已有 Runtime Probe 仅保留为先期风险探针。
- 未通过真实 Godot 技术门禁，不开始端到端使用场景 MVP。
- 技术验证失败先修正 Adapter、合同或 Provider 选择，不通过增加 Agent 掩盖缺口。
- MVP 失败回到最小责任点：讨论决定、查询、规格、素材、绑定、实现或证据。
- 只有 MVP 证明通用价值后，候选才通过人工 Promotion Gate 进入稳定目录。

## 与既有决策的关系

本 ADR 进一步限定 [ADR-003](ADR-003-project-incubated-agent-enhancement-layer.md) 和
[ADR-005](ADR-005-framework-local-lab-before-game-project.md) 的开发顺序。它不取消真实项目
验证和人工晋升，也不否定已经完成的 Lab Probe；它要求在完整 MVP 前先冻结最小理论边界，
并把 Godot 技术可行性与用户场景价值分开验收。

## 备选方案

### 一开始就在真实项目中同时搭框架和接 MCP

反馈最直接，但失败归因困难，且容易把项目路径、玩法和 Provider 工具名固化到公共合同，拒绝。

### 理论框架完成后直接进入端到端 MVP

步骤较少，但 MCP 安装、Godot 导入和运行故障会污染对框架语义的判断，拒绝。

### 先把所有 Godot MCP 都接入再设计框架

可以获得较宽工具覆盖，但公共语义会被 Provider 能力反向塑造，并产生无必要的适配成本，拒绝。

## 后果

- 每一层失败都更容易归因和修正。
- 前期需要投入合同、行为用例和假 Adapter，短期内不会展示完整游戏生成效果。
- 已有 Godot Runtime Probe 保留，但不再决定理论框架的任务顺序。
- godot-ai 是首个实测 Provider，不是公共 Skill 或 Contract 的依赖。
- MVP 成为第一轮产品价值门禁，GameJam 则继续承担更复杂真实制作与晋升验证。
