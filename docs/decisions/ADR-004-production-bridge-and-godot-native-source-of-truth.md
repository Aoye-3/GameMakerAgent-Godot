# ADR-004：以 Production Bridge 连接玩法、素材生产与 Godot 原生实现

## 状态

Accepted

## 日期

2026-09-01

## 与既有决策的关系

本决策澄清 ADR-003 中“引擎中立”的含义：公共意图与证据语义不依赖具体 MCP，但首个产品
和验证环境明确采用 Godot-first，不为了理论上的跨引擎兼容退化为最低公分母模型。ADR-003
其余项目孵化、Provider 可替换和人工晋升决定保持有效。

## 背景

ADR-003 确立了 GameMakerAgent 是项目孵化、Provider 可替换的 Agent 增强层，但只描述
顾问、职责链、运行证据和晋升还不够。VibeGame 的另一项关键价值，是用统一语义连接
玩法设计、场景结构、代码、素材规格、动画、Pivot、碰撞和资源引用，使不同生产环节
不会各说各话。

Godot 已经提供成熟的 Scene、Resource、导入器和运行时，godot-ai 等 MCP 也能执行大量
编辑与运行操作。重新实现一套跨引擎场景树会与 Godot 形成两个真实源；但如果完全让
模型在每次任务中临时推断，又会留下稳定的信息差：生图结果不知道如何切帧、定 Pivot、
配置导入、绑定 Resource、连接碰撞和进入实际场景，最终只能以“图片生成成功”代替
“内容已在游戏中正确工作”。

## 决策

1. GameMakerAgent 的产品定位进一步明确为：**Godot-first、Provider-neutral 的游戏生产
   语义与验证层，为 Codex 等通用编码 Agent 补足跨玩法、素材和引擎的协作信息。**
2. 框架新增 `Production Bridge` 架构边界，把三种语言连接起来：
   - 玩法语言：玩家体验、玩法目的、关卡节奏和验收结果；
   - 素材语言：视觉意图、尺寸、帧、格式、透明度、Pivot、生成来源和许可；
   - Godot 语言：Resource 类型、导入选项、场景节点、动画、碰撞和绑定位置。
3. Godot 原生项目继续是场景、节点、脚本、Resource 和导入结果的唯一真实源。GameMaker
   只保存任务局部的生产意图、约束、绑定计划和验证结果，不镜像完整 SceneTree，也不定义
   第二套物理、动画或资源运行时。
4. 首版 Production Bridge 由四类轻量制品组成，名称和字段在项目实测前保持 Draft：
   - `Project Semantic Model`：按需查询项目已有玩法、技术和美术约定；
   - `Production Card`：把一次内容需求收敛为玩家结果、复用计划、新素材和验收证据；
   - `Asset Spec`：把素材意图转成可生成、可后处理、可导入的技术规格；
   - `Godot Binding`：说明素材将成为哪类 Resource、进入哪个场景位置以及如何验证。
5. 生图、图像编辑、音频或 3D 生成能力是 `Asset Provider`；godot-ai、其他 MCP、Godot CLI
   或 EditorPlugin 是 `Authoring / Runtime Provider`。Provider 实现可以替换，上层生产制品
   不出现第三方工具名。
6. Production Bridge 与交付验证是两条相连但可独立使用的链：

   ```text
   Production Bridge: 玩法决定 -> 内容规格 -> 素材规格 -> Godot 绑定
   Delivery Loop:      任务契约 -> 实现 -> 运行 -> 证据 -> 审核
   ```

7. 专业知识继续保持按需、低噪声。首版最多形成三个用户可见技能包：
   `studio-advisor`、`game-delivery`、`evidence-review`。Production Bridge 的契约、项目查询和
   Provider 适配不是常驻“角色”，普通编码任务不加载完整玩法或美术讨论。
8. Asset Spec 和 Godot Binding 必须在首个真实“新增关卡或内容”纵切片中共同验证，不能
   只用 Schema 完整度宣称成立。字段稳定后再晋升为 `docs/contracts/` 和机器可读 Schema。

## 备选方案

### 只做顾问、编排和运行证据层

实现较轻，但会丢失 VibeGame 连接代码、素材和玩法的核心价值，素材生成到 Godot 使用的
信息差仍由每次 Agent 临时填补，拒绝。

### 把 VibeGame 的 Project、Scene、Node JSON 直接迁移到 Godot

可以保留显式语义，但会复制 Godot 已经成熟的 Scene 和 Resource 模型，产生同步成本与
双真实源，拒绝。只提炼 Pivot、帧、碰撞、语义资源键和跨文件引用等关系。

### 直接采用 GameStudio 的资产文档与完整专业团队

其 Art Bible、Asset Spec、资产清单和技术美术审查有参考价值，但大量阶段、角色、确认和
模板会进入普通开发上下文，而且公开链路没有稳定覆盖生成后处理、Godot 导入绑定和运行
验证，拒绝整体采用；只提炼能形成契约或检查器的专业判断。

### 将生图能力或 godot-ai 固定为框架依赖

短期接入更快，但会把公共语义绑定到单一服务、认证方式和工具名称，拒绝。它们作为首批
Provider 和实测对象。

## 后果

- Asset Contract 从远期辅助能力提前为首个生产纵切片的核心依赖。
- GameMaker 的差异不再是“更多 Agent”或“更多 Godot 工具”，而是可追踪的跨域翻译和
  证据闭环。
- 需要控制语义模型规模；任何字段都必须回答它减少了哪类返工、错误或验证盲区。
- 需要分别验证 Provider 一致性和最终游戏结果，工具调用成功不能替代场景内验收。
- 首版以 Godot 为验证环境，但稳定契约不得依赖 godot-ai 的工具名；其他引擎适配只有在
  真实需求出现后才开展。
