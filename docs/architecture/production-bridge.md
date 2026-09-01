# Production Bridge：从玩法与素材意图到 Godot 可运行内容

## 架构状态

本文描述 [ADR-004](../decisions/ADR-004-production-bridge-and-godot-native-source-of-truth.md)
已经接受的边界。具体字段、Schema 和 Provider 实现仍处于项目验证前的 Draft，不应被描述
为框架已经提供的稳定能力。

## 定位

Production Bridge 是 GameMakerAgent 的生产语义层。它不生成一套替代 Godot 的游戏项目，
而是让通用编码 Agent 能回答一条完整问题：

> 为了实现这项玩家体验，需要复用或新增什么内容；新素材应以什么规格生产；它在 Godot
> 中如何导入、绑定和运行；用什么证据证明结果确实成立？

```text
Human / Advisor
  -> Gameplay Intent
  -> Production Card
      -> Reuse Plan
      -> Asset Spec -> Asset Provider -> Normalized Artifact
      -> Godot Binding -> Authoring Provider -> Native Godot Project
  -> Run Recipe -> Runtime Provider -> Evidence Bundle -> Reviewer
```

## 三种语言的连接

| 语义域 | 典型问题 | Production Bridge 输出 |
| --- | --- | --- |
| 玩法 | 玩家在这一关做什么、感受什么、何时算完成 | 玩家结果、关卡节拍、交互和验收条件 |
| 素材 | 需要什么视觉对象，如何保持风格与技术一致 | 复用/新增决定、生成提示、尺寸、帧、格式、Pivot、来源 |
| Godot | 素材如何成为可运行的场景内容 | Resource 类型、导入设置、节点/属性绑定、动画、碰撞、验证探针 |

这个转换必须是双向可追踪的：运行失败能回到具体绑定或素材约束，而不是只得到“画面不对”；
设计变更也能识别受影响的资产和 Godot 绑定，而不是重做整个项目。

## 核心制品

### Project Semantic Model

它是对原生项目的**轻量、可查询视图**，不是另一份项目模型。首版只按任务读取：

- 技术约定：Godot 版本、语言、目录、命名、输入、分辨率和导入惯例；
- 玩法语义：已有系统、玩家动词、胜负和可观测状态；
- 场景模式：可复用场景、挂点、组、信号和资源组织方式；
- 美术语义：视觉规则、资产类别、尺寸层级、Pivot 与动画惯例。

任何可直接从 Godot 项目可靠查询的事实不长期复制。缓存必须携带源 revision，并可以丢弃
重建。

### Production Card

Production Card 是单个内容任务的交接面，不是完整 GDD。建议包含：

- `player_outcome`：玩家可感知的结果；
- `content_beats`：关卡或功能的最小节拍；
- `reuse_plan`：优先复用的场景、脚本和资源；
- `new_assets`：真正需要新增的素材及原因；
- `godot_bindings`：预期 Resource、场景位置和行为连接；
- `acceptance`：静态、运行状态、运行视觉和人工手感证据。

讨论不是强制前置。如果请求清楚，交付技能可以直接形成最小 Production Card；只有创意
取舍未确定时才调用 Studio Advisor。

### Asset Spec

Asset Spec 负责把视觉或声音意图变成生产约束。不同资产类型字段不同，但至少要覆盖：

- 游戏内职责和视觉描述；
- 像素尺寸或几何预算、格式、透明度、色彩空间；
- 帧布局、FPS、循环、Pivot、切片或碰撞提示；
- 生成/编辑来源、许可证和可复现参数；
- 归一化步骤与 Godot 导入预期；
- 最终引用位置和验证方式。

生成提示只是 Asset Spec 的一个字段。图像生成成功不代表 Asset Spec 完成；只有归一化、
导入、绑定和验证全部可追踪，素材才进入 `usable` 状态。

### Godot Binding

Godot Binding 只描述这次任务的增量关系，例如：

- 文件将导入为 `Texture2D`、`SpriteFrames`、`TileSet`、`AudioStream` 或其他 Resource；
- 导入选项、区域切分、过滤、压缩和循环设置；
- 绑定到哪个稳定场景入口、节点职责、属性或资源槽；
- Pivot、碰撞、动画和脚本信号如何对齐；
- 用哪组输入、状态探针和截图位置验证。

Binding 不保存完整 SceneTree；最终绑定事实以 `.tscn`、`.tres`、`.import`、脚本和 Godot
运行行为为准。

## Provider 边界

| Provider | 负责 | 不负责 |
| --- | --- | --- |
| Asset Provider | 按规格生成或编辑图像、音频、3D 等原料 | 决定玩法、偷偷改变技术规格、宣称 Godot 内可用 |
| Normalizer | 切片、裁剪、命名、格式转换、元数据检查 | 改写美术方向或场景结构 |
| Authoring Provider | 编辑 Godot 场景、脚本、资源和导入设置 | 定义 GameMaker 公共语义 |
| Runtime Provider | 启动、输入、推进、观测、截图和诊断 | 单独决定玩法体验是否合格 |
| Reviewer | 按 revision 与证据给出 verdict | 修复实现或复用旧证据 |

内置图像生成能力可以作为 Asset Provider；godot-ai 可以同时承担 Authoring Provider 和
Runtime Provider。更换其中任一 Provider 不应要求修改 Production Card 的玩法结果。

## “新增关卡”的典型运行逻辑

1. Agent 查询已有玩家动词、关卡入口、可复用资源与视觉约定。
2. 将用户请求收敛为最小 Production Card；不确定的创意取舍才进入顾问讨论。
3. 先制定复用计划，再为缺失内容建立 Asset Spec，避免无意义生成。
4. Asset Provider 生成原料，Normalizer 检查尺寸、帧、透明度、命名与来源。
5. Authoring Provider 按 Godot Binding 导入、创建 Resource 并接入原生场景。
6. Runtime Provider 执行 Run Recipe，收集状态、截图、日志和源 revision。
7. Reviewer 分别判断静态、状态和视觉证据；手感与创意质量保留人工最终判断。
8. 失败回到最小责任点：玩法规格、素材、归一化、绑定或实现，而不是重跑整个“工作室”。

## 噪声与规模边界

- 普通代码修复不加载 Art Bible、关卡理论或完整资产清单。
- 项目语义按任务查询，不在每次提示中注入全量快照。
- 专业判断优先固化为字段约束、检查器和示例；只有存在真正取舍时才启用顾问视角。
- 不按“开发阶段”维护全局状态机；状态由当前制品与证据自然导出。
- 不追求跨引擎最低公分母。首版用 Godot 验证稳定语义，其他引擎通过 Adapter 再映射。

## 成熟度门禁

Production Bridge 只有在同一真实内容纵切片中完成以下链路后，才允许形成稳定契约：

```text
用户需求
  -> Production Card
  -> 至少一个新增或修改素材
  -> Godot Resource / Scene 绑定
  -> 可重复运行与证据
  -> 人工确认玩家结果
```

只验证 JSON 可解析、MCP 调用成功或图片文件存在，都不足以通过门禁。
