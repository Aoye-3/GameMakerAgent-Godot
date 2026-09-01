# GameMakerAgent

让 Codex 等通用编码 Agent 理解如何把**玩法设计、素材生产、Godot 实现与运行验证**连接成
一条可信的游戏开发链路。

> **当前状态：架构落地起步阶段。** V1 的产品边界、ADR、核心契约草案和实施计划已经建立；
> Production Bridge、Godot Provider 和完整内容纵切片尚未实现。当前仓库不是可安装的成品，
> 也不应把设计目标理解为已经交付的能力。

## 为什么需要 GameMakerAgent

Codex、Claude Code 等编码 Agent 已经能够修改 Godot 项目；godot-ai、Godot MCP 和编辑器插件
也能提供场景编辑、输入、截图和日志。但真实游戏制作仍存在一段没有被工具本身解决的信息差：

```text
“设计一个新关卡”
  -> 这个关卡要带来什么玩家体验？
  -> 应该复用哪些系统、场景和素材？
  -> 新素材需要什么尺寸、帧、Pivot、透明度和风格？
  -> 生成结果如何成为 Godot Resource 并绑定到实际场景？
  -> 如何证明玩法状态和最终画面都符合要求？
```

单独的代码 Agent、素材生成器或 Godot MCP 都只覆盖其中一部分。GameMakerAgent 要补的是
这些工具之间的**生产语义、交接契约和验证闭环**。

## 项目定位

GameMakerAgent 是一个 **Godot-first、Provider-neutral 的 Agent 增强层**：

- **Godot-first**：V1 以原生 Godot 项目完成真实验证，优先利用 Godot 开源生态；
- **Provider-neutral**：godot-ai、其他 MCP、Godot CLI 和素材生成服务位于可替换 Adapter 后；
- **Agent enhancement**：增强 Codex 等现有 Agent，不训练或包装一个封闭的专用模型；
- **Production semantics**：统一玩法、代码、场景、素材规格和验收证据的语言；
- **Evidence-driven**：工具调用成功不等于内容完成，最终判断必须关联运行结果和源 revision。

GameMakerAgent **不是**：

- 新的游戏引擎或 Godot SceneTree 替代品；
- 另一套覆盖所有 Godot 操作的全能 MCP；
- 强制用户进入固定阶段、固定团队和大量模板的虚拟工作室；
- 素材生成平台本身；
- 能自动判断“是否好玩”的伪客观评分器。

## 核心架构

V1 由两条相连、但可以独立使用的链组成。

### Production Bridge

把创意和素材意图翻译为 Godot 可以消费的内容规格：

```text
玩法意图
  -> Project Semantic Model
  -> Production Card
  -> Asset Spec
  -> Asset Provider / Normalizer
  -> Godot Binding
  -> 原生 Godot Resource / Scene
```

### Delivery Loop

把“实现完成”变成有证据、可复验的结论：

```text
任务契约
  -> Maker 实现
  -> Runtime Provider 运行与输入
  -> Evidence Bundle
  -> Reviewer verdict
  -> 修复或人工确认
```

完整协作关系：

```text
Human / Codex
      |
      v
GameMakerAgent
  ├─ Studio Advisor       可选的玩法、体验、范围与复盘顾问
  ├─ Production Bridge    内容、素材和 Godot 绑定语义
  ├─ Delivery Loop        实现、运行、证据和审核职责
  └─ Promotion Gate       从真实项目晋升可复用能力
      |
      +---------------------------+
      |                           |
      v                           v
Asset Providers             Godot Providers
image generation / edit     godot-ai / MCP / CLI / plugin
      |                           |
      +-------------+-------------+
                    v
            Native Godot Project
              唯一运行真实源
```

详细边界见 [Production Bridge](docs/architecture/production-bridge.md) 与
[Agent 增强层](docs/architecture/agent-enhancement-layer.md)。

## V1 核心制品

| 制品 | 作用 | V1 边界 |
| --- | --- | --- |
| Project Semantic Model | 按任务查询项目的玩法、技术、场景和美术约定 | 可丢弃查询视图，不复制完整 SceneTree |
| Production Card | 描述本次内容的玩家结果、节拍、复用、新素材和验收 | 不是完整 GDD，不强制经过顾问讨论 |
| Asset Spec | 描述素材职责、视觉要求、尺寸、帧、Pivot、格式、来源和许可 | 生成提示只是其中一个字段 |
| Godot Binding | 描述 Resource 类型、导入选项、场景位置、动画/碰撞和验证点 | 最终事实仍是原生 Godot 文件与运行行为 |
| Evidence Bundle | 关联输入、状态、截图、诊断、Provider 和源 revision | 过期或不完整证据不能通过 |
| Promotion Manifest | 记录能力从具体项目进入框架的来源、许可和门禁 | 不进行无人工审批的自动自我扩张 |

Production Card、Asset Spec 和 Godot Binding 当前仍是待真实纵切片验证的设计制品，字段
稳定后才会进入正式 Contract 与 Schema。

## 典型场景：让 Codex 制作一个新关卡

1. Codex 通过 Project Semantic Model 查询现有玩家动词、关卡入口、可复用场景与视觉约定。
2. 如果玩法取舍尚不清楚，用户显式启用 Studio Advisor；请求清楚时直接继续。
3. GameMaker 形成最小 Production Card，先决定复用什么，再列出真正缺失的素材。
4. Asset Spec 把游戏内职责翻译为生成规格、技术限制、来源和归一化要求。
5. 图像生成或编辑能力作为 Asset Provider 产生原料；检查器验证尺寸、帧、透明度和命名。
6. Godot Binding 指导 godot-ai 或其他 Authoring Provider 完成导入、Resource 创建和场景绑定。
7. Runtime Provider 执行输入、状态观察、截图与诊断，形成关联当前 revision 的证据。
8. Reviewer 分别判断静态、运行状态和运行视觉；玩法手感与创意质量由人类最终确认。

失败应回到最小责任点——玩法规格、素材、归一化、Godot Binding 或实现——而不是重跑一个
庞大的“工作室流程”。

## 与现有项目如何协作

| 项目类型 | GameMaker 的关系 |
| --- | --- |
| godot-ai / Godot MCP | 作为 Authoring 或 Runtime Provider 使用，不重新实现同等工具面 |
| 图像、音频、3D 生成工具 | 作为 Asset Provider 使用，通过 Asset Spec 接收约束 |
| GameStudio 类项目 | 选择性提炼专业知识，不复制大量 Agent、阶段和强制模板 |
| Godot 原生项目 | 保存真实场景、资源、脚本、素材和项目级设计事实 |
| Codex / Claude Code | 作为运行 GameMaker 能力的宿主 Agent，负责实际推理与实现 |

更完整的固定版本对比见
[Agentic 游戏生产框架调研](docs/research/agentic-game-production-architecture-study.md)。

## 第一版实施范围

V1 只实现能证明核心价值的最小垂直路径：

1. 验证项目内的 `studio-advisor` 候选，确认它只在讨论时启用；
2. 建立最小 Project Semantic Model 查询能力；
3. 起草并实测 Production Card、Asset Spec 和 Godot Binding；
4. 实现 Runtime Adapter、Evidence Bundle 与最小 Reviewer 闭环；
5. 固定版本实测 godot-ai，并保留 CLI 或其他 Provider 的替换路径；
6. 接入至少一个 Asset Provider；
7. 在真实 Godot 项目中完成一个包含新增或修改素材的关卡/内容纵切片；
8. 将通过项目验证的通用部分去项目化，晋升回本仓库。

V1 不追求多引擎、多模型编排、大型 UI、自动生成完整游戏或完整专业岗位目录。

## 当前进度

| 能力 | 状态 |
| --- | --- |
| 框架仓库与具体游戏项目边界 | 已接受并记录 |
| 原生 Godot 项目是真实源 | 已接受并记录 |
| Runtime Adapter | Draft 0.1 |
| Evidence Bundle / Promotion Manifest | Draft 0.1 + Schema 草案 |
| Studio Advisor | 项目候选已建立，等待真实使用验证 |
| Production Bridge 架构 | 已接受，尚未实现 |
| Production Card / Asset Spec / Godot Binding | 待项目纵切片起草与验证 |
| godot-ai Provider | 已完成源码评估，待固定版本实测 |
| Asset Provider | 待实现 |
| 完整新关卡闭环 | 待实现 |

当前状态以 [实施计划](docs/plans/framework-evolution-plan.md) 为准。

## 仓库结构

```text
GameMakerAgent/
├─ docs/
│  ├─ architecture/    已接受的架构边界
│  ├─ contracts/       跨角色、跨 Provider 的稳定接口
│  ├─ decisions/       ADR 与不可轻易逆转的决策
│  ├─ plans/           实施顺序、状态和验收标准
│  └─ research/        有固定来源和日期的外部调研
├─ schemas/            已形成机器可读草案的契约
├─ skills/             首个能力通过晋升门禁后创建
├─ adapters/           首个 Provider 实现通过门禁后创建
└─ evals/              首个去项目化回归夹具通过门禁后创建
```

不存在的稳定目录不会提前创建空骨架。新能力先在具体项目中验证，再通过 Promotion Gate
进入本仓库。

## 开始参与 V1 实现

目标仓库：[`Aoye-3/GameMakerAgent`](https://github.com/Aoye-3/GameMakerAgent)

```bash
git clone https://github.com/Aoye-3/GameMakerAgent.git
cd GameMakerAgent
```

当前没有需要安装的运行时依赖或可执行 CLI。开始实现前建议依次阅读：

1. [技术文档入口](docs/README.md)
2. [ADR-004：Production Bridge](docs/decisions/ADR-004-production-bridge-and-godot-native-source-of-truth.md)
3. [框架演进计划](docs/plans/framework-evolution-plan.md)
4. [Runtime Adapter](docs/contracts/runtime-adapter.md)
5. [Evidence Bundle](docs/contracts/evidence-bundle.md)

实现必须遵守三条底线：

- 不把具体游戏的玩法、关卡、素材或私有路径写入框架仓库；
- 不让公共 Skill 或 Contract 依赖 godot-ai 等第三方工具名称；
- 不以文件存在、图片生成成功或 MCP 调用成功代替真实运行验证。

## V1 成功门禁

第一版不是以目录数量或 Skill 数量验收，而是以一个真实内容纵切片验收：

```text
用户提出内容需求
  -> Agent 正确理解项目语义
  -> 形成最小生产规格
  -> 生成或修改至少一个素材
  -> 素材正确进入 Godot Resource / Scene
  -> 可重复运行并产生新鲜证据
  -> 人类确认玩家结果成立
```

只有这条链比“Codex + Godot MCP + 生图工具直接开发”实际减少了返工、遗漏或上下文噪声，
GameMakerAgent 的核心假设才算得到第一轮验证。

## 文档与决策

- [框架技术文档](docs/README.md)
- [架构决策记录](docs/decisions/README.md)
- [框架契约](docs/contracts/README.md)
- [开源项目调研](docs/research/open-source-landscape.md)
- [框架与项目仓库边界](docs/architecture/repository-boundaries.md)
