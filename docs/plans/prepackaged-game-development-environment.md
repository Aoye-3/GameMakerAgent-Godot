# 执行计划：预打包的 Codex + Godot 游戏开发环境

## 状态

Active — 本文是 V1 产品终态、工程边界和执行门禁的权威计划。任务完成状态仍同步到
[框架演进计划](framework-evolution-plan.md)，两者冲突时先按
[ADR-007](../decisions/ADR-007-prepackaged-codex-godot-context-environment.md) 修正旧计划。

## 要解决的问题

1. 单独使用 Codex + Godot MCP 时，执行能力充足，但缺少游戏策划、范围、玩法、技术美术与
   可玩性验证语境。
2. 单独使用游戏 Skill 时，建议容易停留在文字层，不能稳定映射到代码、场景、输入、素材和
   验收。
3. 素材生成与 Godot 需求割裂，尺寸、帧、透明度、Pivot、碰撞、导入方式和代码引用缺少统一
   交接面。

## V1 产品终态

```text
Codex                         唯一 Agent Runtime 与编排者
  -> GameMaker Skills         策划、交付、审核语境
    -> Context Core           查询、校验、裁剪、记录和证据检查
      -> Asset Provider       成熟素材生产工具
      -> Godot MCP            成熟 Authoring / Runtime 工具
        -> Native Godot       项目与实现真实源

.vibegame 结构化开发记录
  -> Codex 按需读取
  -> 只读 Godot Dock 展示
```

GameMakerAgent 不建设 Codex 替代品、Agent Runtime、完整 Godot MCP、生成模型或独立创作前端。

仓库内可安装交付包含：

- repo-scoped Codex Plugin；
- `studio-advisor`、`game-delivery`、`evidence-review` 三个 Skill；
- Python 3.11+ Context Core 与 `gamemaker` CLI；
- JSON Schema 和跨制品引用检查；
- Provider capability profile；
- 只读 Godot Dock；
- 去项目化 Fixture、conformance tests、安装诊断与回归入口。

## 核心制品与闭合关系

```text
Decision Card
  -> Project Semantic Model
  -> Production Card
    -> Asset Spec
      -> Normalized Asset
        -> Godot Binding
          -> Implementation Record
            -> Evidence Bundle
```

- 策划判断进入 Decision Card。
- 当前功能目标、复用、新素材和验收进入 Production Card。
- 素材的游戏职责、视觉风格和技术限制进入 Asset Spec。
- 导入、Resource、节点、动画、碰撞和验证点进入 Godot Binding。
- 实际修改的场景、脚本和 Resource 进入 Implementation Record。
- 输入、状态、截图、诊断、Provider 和 source revision 进入 Evidence Bundle。
- 孤立图片、未引用代码、没有验收证据的建议或工具调用不算完成。

公共制品必须带 `schema_version`、稳定 ID、来源和 revision，不得出现第三方 MCP 工具名。
JSON Schema Draft 2020-12 是结构真相；Python 不维护第二套领域模型。

## 项目结构化开发记录

```text
.vibegame/gamemaker/
  environment.json
  index.json
  work/<work_id>/
    decision.md
    project-context.json
    production-card.json
    asset-specs/
    normalized-assets.json
    godot-bindings/
    implementation.json
    evidence/
  artifacts/
```

- 只保存已确认决定和执行结果，不保存完整聊天。
- 轻量 JSON/Markdown、索引和证据元数据进入 Git。
- 截图、视频和原始日志位于忽略的 `artifacts/`，通过摘要、相对路径和哈希引用。
- `index.json` 是可重建投影，不是全局阶段状态机。
- Godot 原生文件始终是实现真相，记录层不复制完整 SceneTree。

## Phase A：可安装环境骨架

1. 在当前仓库原地分支开发，禁止 worktree、克隆和替代目录。
2. 建立 `pyproject.toml`、`src` layout、`uv.lock`、pytest 和 ruff。
3. 所有 `.venv`、缓存、Godot 用户数据和产物留在当前 F 盘工作区。
4. 建立 CLI：`doctor`、`query`、`validate`、`record`、`context`、`rehearse`、
   `provider check`、`evidence review`。
5. `doctor` 只检查并报告 Python、Godot、Plugin、Skill、Dock、MCP profile、项目和工作记录；
   不安装或修改第三方产品。
6. 保持已有 Studio Advisor 用例和 Godot 4.7.2 Runtime Probe 通过。

**门禁：** 锁定依赖可重建；一个命令能判断环境是否准备完成；测试后无意外工作树改动。

## Phase B：语境与代码桥

1. Project Semantic Model 按任务查询 Godot 版本、入口、输入、相关场景/脚本/Resource、可复用
   玩家动词和资产惯例；每条事实带来源与 revision，不返回完整 SceneTree。
2. 建立 Decision Card、Project Context、Production Card、Asset Spec 2D、Godot Binding、
   Implementation Record、Provider Capability Profile 和 Work Index Schema。
3. Context Pack 只把已确认决定、任务局部项目事实、素材结果、Binding 和验收交给编码 Agent；
   不传完整讨论记录或全量项目知识。
4. 跨制品引用必须闭合：新素材被 Binding 引用、Binding 定位 Godot Resource/Node、实现记录
   反查 Production Card、证据反查实现 revision。
5. 完成三个 Skill 与讨论、清晰交付、普通修错、已有功能复验四类路由用例。
6. 两个假 Provider 使用相同合同覆盖成功、超时、能力缺失、素材失败、运行失败和证据过期。

**Checkpoint 1：** 确认决定在假 Provider 上可以完整流转到实现与证据；更换 Provider 不改变
上层语义；普通修错不加载顾问和全量游戏知识。

## Phase C：素材生产与 Godot Binding

1. V1 Asset Spec 只覆盖 2D PNG/精灵，字段包括用途、玩家可见职责、风格摘要、尺寸、帧、
   透明度、Pivot、trim、碰撞对齐、格式、稳定 `asset_id`、来源、许可和归一化规则。
2. Asset Checker 校验 Schema、文件、像素、通道、帧布局、Pivot/trim、来源和许可，并区分
   blocking 与 advisory。
3. Godot Binding 表达 `res://` 路径、Texture2D/SpriteFrames、Import 设置、节点位置、Pivot、
   scale、collision、animation 和运行验收点。
4. 原始素材通过归一化和检查后才能交给 Codex/Godot MCP；替换素材保持稳定 ID 与 Binding。

**门禁：** 一张素材可以从确认风格反查到 Asset Spec、归一化文件、Godot Binding、实际节点
和运行截图。

## Phase D：成熟 Godot MCP

1. 首测固定 revision 的 godot-ai，只在 Adapter profile 内保存 Provider 与工具映射。
2. 受限能力为连接已有项目、场景/脚本/Resource、素材导入、运行、输入、观察、截图、日志、
   停止和清理。
3. Codex 调用 MCP；Python Core 不成为第二套编排器。
4. 统一错误为 `unsupported_capability`、`permission_denied`、`timeout`、
   `provider_unavailable`、`execution_failed`、`stale_evidence`。
5. 不支持 pause、deterministic step 或 `step_until` 时显式降级，不伪造能力。
6. 相同 Fixture 连续执行两次 conformance matrix；只有阻断缺口才比较另一个成熟 Provider。

**Checkpoint 2：** 成熟 MCP 可以执行公共制品，且 Skill、Schema 和 Context Pack 不依赖其工具名。

## Phase E：只读 Godot Dock

Dock 读取 `.vibegame/gamemaker/index.json` 及其引用，展示当前功能目标、确认风格、素材规格、
实现摘要、Provider 能力、最近错误、证据裁决和 revision 新鲜度。

Dock 不得聊天、修改规格、生成素材、编辑场景、启停运行、写入或修复文件。测试比较加载前后
项目文件哈希，证明只读边界。

## Phase F：端到端产品 MVP

用户先通过原生 Godot Project Manager 人工创建空项目；自动链路从已有原生项目开始。

固定纵切片：Godot 4.7.2、GDScript、单场景、四方向俯视移动；角色接触目标后
`items_collected` 从 `0` 变为 `1` 且目标消失；唯一生成素材是 Fixture 专属 64×64 RGBA
角色精灵，该尺寸不成为公共默认值。

执行顺序：

1. Advisor 确认玩家目标、范围和素材风格。
2. Query 记录原生项目 baseline revision。
3. 形成 Production Card、Asset Spec 和 Godot Binding。
4. 成熟 Asset Provider 生成图片，Core 检查并归一化。
5. Codex 根据 Context Pack 调用成熟 Godot MCP 完成场景、代码、输入、Resource 与碰撞。
6. Runtime Provider 执行输入并收集状态、截图和诊断。
7. Reviewer 审查实现与证据，记录写入 `.vibegame/gamemaker/` 并由 Dock 展示。
8. 故意制造一次素材不合规或证据过期并确认拒绝；修复后复验。
9. 在同一项目再次执行，确认没有重复节点、输入或漂移引用。

**Checkpoint 3：** 人工确认相较直接使用 Codex + Godot MCP，环境确实减少策划缺位、上下文
丢失、素材/代码错位和无证据完成。

## 发布门禁与 V1 排除项

Checkpoint 3 通过后，才把 Skill、Core、Schema、Provider profile 和 Dock 从 Lab 晋升，创建
repo-scoped Plugin，版本定为 `0.1.0`。只声明 Windows、Godot 4.7.2、Python 3.11+、2D 和
GDScript 已验证，不发布 PyPI 或公共插件目录。

V1 不做：独立 Agent Runtime、自研完整 Godot MCP、多 Agent 调度、自动创建 Godot 项目、3D、
C#、多引擎、Web 创作台、可写 Dock、完整聊天归档，以及未经纵切片验证的大规模 Skill 搬运。

## 下一执行项

先完成 Phase A 工程骨架，再实现 Project Semantic Model 与跨制品 Context Pack；暂不增加更多
MCP 或游戏 Skill 数量。
