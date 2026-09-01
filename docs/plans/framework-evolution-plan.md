# 实施计划：GameMaker V1 三层验证演进

## 状态

Active

> **产品语义基线：** V1 的产品终态、安装形态、结构化开发记录和人工创建原生 Godot 项目的
> 最新决策见 [预打包游戏开发环境执行计划](prepackaged-game-development-environment.md) 与
> [ADR-007](../decisions/ADR-007-prepackaged-codex-godot-context-environment.md)。本文继续维护任务
> 状态；旧文字若与 ADR-007 冲突，应在对应任务实施时按该决策修正。

## 目标

先建立可演练的理论框架，再独立验证真实 Godot 与 Provider 技术能力，最后执行一条从讨论、
查询、素材生成到 godot-ai 创建原生项目、完成代码基础和嵌入素材的使用场景 MVP。MVP 通过后，
再以 TapTapGameJam 的真实制作过程验证复杂场景和能力晋升。

## 成功标准

- TapTapGameJam 始终是可直接由 Godot 打开的原生项目。
- Player 和 Reviewer 能依据可回放输入、结构化状态、截图和诊断形成闭环。
- 一次新增内容能从玩家结果进入素材规格、Godot Resource / Scene 绑定和运行证据，且不
  需要 Agent 临时猜测关键导入约束。
- 项目能力只有通过 Promotion Gate 后才成为 GameMaker 的稳定资产。
- GameMaker 不依赖 TapTapGameJam 的路径、玩法、资产或私有状态。
- 两套 Doc 分别保持可导航、无职责混写，并与实际实现同步。
- 理论框架、Godot 技术可行性和使用场景价值分别验收，失败能回到明确责任层。

## 已接受的架构决策

- [ADR-001](../decisions/ADR-001-separate-framework-and-project-repositories.md)：双仓独立、项目驱动晋升。
- [ADR-002](../decisions/ADR-002-native-godot-project-and-replaceable-control-adapter.md)：原生 Godot 项目与可替换 Runtime Adapter。
- [ADR-003](../decisions/ADR-003-project-incubated-agent-enhancement-layer.md)：项目 `.vibegame` 孵化 Agent 增强层，验证后晋升。
- [ADR-004](../decisions/ADR-004-production-bridge-and-godot-native-source-of-truth.md)：以 Production Bridge 连接玩法、素材和 Godot 原生实现。
- [ADR-005](../decisions/ADR-005-framework-local-lab-before-game-project.md)：GameJam 前在框架本地 Lab 搭建通用底座。
- [ADR-006](../decisions/ADR-006-theory-framework-before-godot-and-scenario-mvp.md)：理论框架、真实 Godot、使用场景 MVP 顺序通过。
- [ADR-007](../decisions/ADR-007-prepackaged-codex-godot-context-environment.md)：Codex 负责编排，GameMaker 连接游戏语境、素材、Godot 实现和证据。

## 依赖关系

```text
已有双仓边界与 Runtime / Evidence / Promotion 契约
  -> 框架本地 Lab + Studio Advisor / Godot Probe 候选
    -> 理论框架：查询、生产制品、技能路由、Delivery Loop、假 Provider 演练
      -> 真实 Godot：固定版本 Provider conformance 与素材绑定技术验证
        -> 使用场景 MVP：讨论 -> 查询 -> 生成素材 -> godot-ai -> 原生项目 -> 代码与素材
          -> GameJam 真实纵切片
            -> 检查器、技能和契约按证据晋升到 GameMakerAgent
```

## 核心参考实现的吸收与接入时机

“源码已拉取”“语义已吸收”“运行时已接入”是三种不同状态。核心参考实现只以固定 Git ref
进入研究基线；只有经过目标任务和回归用例证明的最小部分才进入 GameMaker 实现。

| 参考实现 | 当前状态 | 吸收或接入时机 | 进入 GameMaker 的形态 | 通过条件 |
| --- | --- | --- | --- | --- |
| VibeGame `7549e57` | Task 1.0 源码吸收清单已完成；Studio Advisor 候选已选择性迁入 | Phase 1.1、1.2、1.4 | 查询语义、Production Bridge 字段、运行/证据合同与用例 | 保留统一语义但不携带 Phaser、阶段状态机或完整运行外壳 |
| Claude Code Game Studios `984023d` | Task 1.0 源码吸收清单已完成，并已与 GameStudio 去重 | Phase 1.2、1.3 | 顾问视角、范围问题、Asset Spec 专业约束 | 只在讨论或规格任务加载，不复制多 Agent、Hook 和强制模板 |
| GameStudio `6027706` | Task 1.0 源码选择与 CCGS 去重已完成 | Phase 1.2、1.3 | 少量技术美术、资产和专业审核规则；优先转成字段或检查器 | 每项规则必须指出减少的错误；不引入 55 Agent / 182 Skill 目录 |
| Godot Gamestudio / Xenodot Forge | 文档研究已完成，非首轮依赖 | Phase 1.4 与 Phase 5 | Evidence 新鲜度、Maker/Reviewer 分离、人工 Promotion Gate | 与现有合同对照后只补缺口，不移植其产品外壳 |
| godot-ai `a468a7e` | Task 1.0 工具面映射已完成；**尚未安装、未实现 Adapter、未接入** | Phase 2.2 安装固定插件并实现 Provider；Phase 3.4 用于 MVP | 受限 Authoring / Runtime Provider，位于 Adapter 后 | 创建/打开、编辑、资源、运行、输入、状态、截图、日志、清理矩阵重复通过 |
| 其他 Godot MCP | 仅研究候选 | godot-ai 在 Phase 2.2 出现阻断缺口后 | 同一 Adapter 的替代 Provider | 必须使用相同 conformance matrix，不因工具更多而接入 |
| GdUnit4 / Benchmarks | 候选研究 | Phase 2.1 补白盒验证；Phase 5 建回归 | 测试依赖或公开回归思想 | 不用 benchmark 分数代替人工玩法结论 |

核心参考吸收必须在 Checkpoint 1 关闭，godot-ai 真实接入必须在 Checkpoint 2 关闭；两者未完成
不得开始 Phase 3 的完整使用场景 MVP。

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

## Phase 0.5：已有框架 Lab 与先期风险探针

### Task 0.4：准备 Studio Advisor 理论候选

**状态：** Completed as candidate — 已迁入 Lab 并通过静态行为用例；真实价值留到 Phase 3。

**验收标准：**

- [x] 单入口按需提供玩法、体验、范围和试玩复盘视角。
- [x] 候选规则明确不创建 Agent、GDD、任务、代码或场景。
- [x] 静态用例覆盖普通实现请求不加载顾问内容。

**验证：** `scripts/test-lab.ps1` 能解析全部 Studio Advisor 行为用例。

**依赖：** Checkpoint 0。

### Task 0.5：建立框架本地 Lab 与 Godot Runtime Probe

**状态：** Completed

**验收标准：**

- [x] `lab/` 明确区分候选、夹具和固定来源，不复制完整外部仓库。
- [x] 本地 Godot 4.7.2 位于 Git 忽略的 `.tools/`，运行数据与缓存留在当前 F 盘工作区。
- [x] 去项目化 Runtime Probe 能验证输入、`gamemaker_watch` 和 `_gamemaker_state()`。
- [x] 一个命令可以运行全部首批 Lab smoke。

**验证：** `powershell -ExecutionPolicy Bypass -File scripts/test-lab.ps1` 输出
`LAB_TEST_PASS`。

**依赖：** Checkpoint 0、ADR-005。

### Checkpoint 0.5：理论工作台可用

- [x] 候选、Fixture、来源和本地工具边界明确。
- [x] 先期 Probe 可用于发现 Godot 基础风险，但不被描述为产品闭环。
- [x] Studio Advisor 仍属于 Lab，不被描述为稳定能力。

## Phase 1：搭建理论框架

本阶段定义 GameMaker 的逻辑系统并用假 Provider 演练，不接入正式 godot-ai，也不要求创建
真实游戏项目。理论框架必须可解析、可路由、可失败，不能只是一组说明文档。

### Task 1.0：完成核心竞品源码吸收清单

**状态：** Completed — 四个核心源码 ref 已完成逐文件 adopt/adapt/reject 取证与去重。

**验收标准：**

- [x] VibeGame、Claude Code Game Studios、GameStudio、godot-ai 固定 revision 可由 Git ref 读取。
- [x] 每个拟吸收能力记录源文件、目标制品或模块、改写方式、许可证和明确拒绝项。
- [x] GameStudio 与 Claude Code Game Studios 的重叠知识完成去重，并优先落为字段、检查器或按需顾问参考。

**实际结果：** [核心竞品源码吸收清单](../research/core-source-intake.md) 固定了后续任务唯一允许
使用的知识入口，并以 `SRC-01` 至 `SRC-06` 为 Skill、Contract、Schema、检查器和 Provider
提供行为追踪锚点。本任务未新增正式能力，也未安装 godot-ai。

**验证：** 四个来源 ref/revision 与许可证可读取；逐文件清单覆盖来源、问题、目标形态、改写和
拒绝项；CCGS/GameStudio 重叠文件已直接 diff；Lab、JSON、文档链接与 Git diff 检查通过。

**依赖：** Checkpoint 0.5。

### Task 1.1：建立 Project Semantic Model 查询合同

**状态：** Completed — Python Query 已覆盖非 Godot、已有项目、任务局部事实、source revision
与过期判断；公共 Schema 和自动化测试已建立。

**验收标准：**

- [ ] 区分空工作区、已有 Godot 项目和过期查询三种状态。
- [ ] 按需返回 Godot 基线、目录、输入、场景入口、可复用资源、玩家动词和资产惯例。
- [ ] 每条事实携带来源与 revision，不复制完整 SceneTree。

**验证：** 用空工作区、已有项目和普通修错三个 Fixture 检查查询最小性与过期行为。

**依赖：** Task 1.0。

### Task 1.2：定义 Production Card、Asset Spec 与 Godot Binding Draft

**状态：** Completed as Draft — 三类 Schema、2D PNG 检查器、Implementation Record 与跨制品
引用审核已实现；真实 Godot 纵切片前不晋升为稳定 1.0。

**验收标准：**

- [ ] Production Card 只保存当前内容的玩家结果、节拍、复用、新素材与验收。
- [ ] Asset Spec 表达尺寸、帧、透明度、Pivot、格式、来源、许可和归一化要求。
- [ ] Godot Binding 表达 Resource、导入选项、场景位置、动画/碰撞和验证点。
- [ ] 三种制品都不出现 imagegen、godot-ai 或其他第三方工具名。

**验证：** 用“空项目创建”和“现有项目新增内容”两套纸面 Fixture 往返追踪字段。

**依赖：** Task 1.1。

### Task 1.3：限定三个技能包与上下文路由

**状态：** Completed as candidate — repo-scoped Plugin 已包含三个 Skill，Context Pack 按 Asset
Provider、Programmer、Reviewer 裁剪，路由正反例已进入回归。

**验收标准：**

- [ ] 用户可见能力只包含 `studio-advisor`、`game-delivery`、`evidence-review`。
- [ ] 清楚请求跳过 Advisor；只有真实创意取舍才加载顾问视角。
- [ ] Programmer 只接收确认决定、任务局部语义和验收，不接收完整讨论记录。

**验证：** 对讨论、普通修错、新项目、已有功能复验四类请求运行路由用例。

**依赖：** Task 1.2。

### Task 1.4：完成假 Provider Delivery Loop

**状态：** In progress — Provider capability、统一错误、素材失败、未绑定素材、过期证据和
unsupported capability 已覆盖；完整成功、超时与运行失败演练仍待收口。

**验收标准：**

- [ ] Asset、Authoring、Runtime Provider 具有工具中立端口和统一错误语义。
- [ ] Maker、Runtime、Reviewer 是逻辑职责，不强制创建多个 Agent。
- [ ] Evidence Reviewer 能区分 PASS、FAIL 和 INSUFFICIENT_EVIDENCE，并拒绝过期证据。

**验证：** 假 Provider 覆盖成功、超时、素材不合规、运行失败和证据版本不一致。

**依赖：** Task 1.3。

## Checkpoint 1：理论框架成立

- [ ] 四个核心参考实现的采用、改写和拒绝清单具有源码证据，未吸收内容不会隐式进入 MVP。
- [ ] 从确认决定到 Production Card、Asset Spec、Godot Binding 和 Evidence 可完整演练。
- [ ] 普通实现没有加载顾问或全量项目知识。
- [ ] 更换假 Provider 不改变上层生产语义。
- [ ] 人工确认理论合同足够进入真实 Godot 技术验证。

## Phase 2：真实 Godot 与 Provider 技术验证

本阶段只回答“理论合同能否由真实 Godot 工具可靠执行”。使用去项目化 Fixture，避免玩法评价
和完整用户旅程干扰技术归因。

### Task 2.1：固定 Godot 基线并完善 Conformance Fixture

**状态：** In progress

**验收标准：**

- [x] Godot 4.7.2 CLI 已在当前工作区完成导入和无窗口运行。
- [x] Runtime Probe 可验证输入和结构化状态。
- [ ] Fixture 同时包含通过、故意失败、截图和诊断预期。

**验证：** 从干净 Fixture 连续运行两次并得到等价状态结果。

**依赖：** Checkpoint 1；已完成项属于先期风险探针，不代表本任务整体提前通过。

### Task 2.2：固定版本实测 godot-ai

**状态：** Pending

**验收标准：**

- [ ] 从 `research/godot-ai/main` 对应 revision 按官方插件结构安装到测试 Fixture，不 vendor 完整仓库。
- [ ] GameMaker Authoring / Runtime Adapter 只暴露理论合同需要的受限能力。
- [ ] 验证项目创建/打开、场景、脚本、资源、运行、输入、状态、截图、日志和清理矩阵。
- [ ] 记录版本、许可证、权限、安全边界、项目污染和失败模式。
- [ ] 只有存在阻断缺口时，才以同一矩阵比较其他 Godot MCP。

**验证：** 从干净 Fixture 重复两次，Authoring 与 Runtime 结果均可追踪到源 revision。

**依赖：** Task 2.1。

### Task 2.3：验证素材到 Godot Binding 的技术路径

**状态：** Pending

**验收标准：**

- [ ] 一个固定测试素材通过尺寸、透明度、命名、来源和许可证检查。
- [ ] godot-ai 按 Godot Binding 完成导入、Resource 创建和场景绑定。
- [ ] 运行截图与结构化状态共同证明素材已在实际场景生效。

**验证：** 删除生成项目后，从相同规格重复执行并得到等价绑定结果。

**依赖：** Task 2.2。

## Checkpoint 2：真实 Godot 技术门禁

- [ ] godot-ai 固定版本已实际安装并通过 Adapter 调用；状态不再只是“源码已拉取”。
- [ ] 理论 Adapter 的关键能力均有真实 Provider 对应或明确降级路径。
- [ ] Godot 项目副产物和 Provider 权限边界可控。
- [ ] 素材进入 Resource / Scene 的路径可以重复执行。
- [ ] 人工确认可以开始端到端使用场景 MVP。

## Phase 3：完整使用场景 MVP

MVP 固定验证以下用户旅程，不在本阶段扩展为通用游戏生成平台：

```text
讨论 -> 查询 -> 生成素材 -> godot-ai MCP -> 创建 Godot 项目 -> 代码基础 -> 嵌入素材 -> 运行证据
```

### Task 3.1：讨论并确认一个小型游戏目标

**状态：** Pending

**验收标准：**

- [ ] 用户显式进入 Studio Advisor，形成一张确认后的 Decision Card。
- [ ] 讨论只解决玩家目标、核心交互和 MVP 范围，不生成完整 GDD。
- [ ] 后续 Maker 不接收完整讨论记录。

**验证：** 对比交接上下文，只包含确认决定而非讨论全文。

**依赖：** Checkpoint 2。

### Task 3.2：查询上下文并形成生产制品

**状态：** Pending

**验收标准：**

- [ ] 查询识别当前为空工作区或不存在目标项目，并返回新项目所需 Godot 基线。
- [ ] 形成最小 Production Card、至少一个 Asset Spec 和对应 Godot Binding。
- [ ] 制品可追踪到 Decision Card 和查询来源。

**验证：** 人工走查不存在关键尺寸、导入、场景入口或验收约束的临时猜测。

**依赖：** Task 3.1。

### Task 3.3：生成并归一化首个素材

**状态：** Pending

**验收标准：**

- [ ] Asset Provider 只接收 Asset Spec 所需字段。
- [ ] 输出通过尺寸、透明度、命名、来源、许可证及适用的帧/Pivot 检查。
- [ ] 归一化制品具有稳定标识，供 Godot Binding 引用。

**验证：** 检查器通过；原始输出与归一化输出来源可追踪。

**依赖：** Task 3.2。

### Task 3.4：通过 godot-ai 创建项目、代码基础并嵌入素材

**状态：** Pending

**验收标准：**

- [ ] godot-ai 创建可由原生 Godot 打开的项目、主场景和最小可玩代码。
- [ ] 归一化素材成为 Godot Resource 并绑定到实际可见节点。
- [ ] 公共制品不记录 godot-ai 工具名，Provider 可替换边界保持成立。

**验证：** 不依赖手工编辑器操作，从干净输出目录重复创建并成功启动。

**依赖：** Task 3.3。

### Task 3.5：运行、审核并给出 MVP 结论

**状态：** Pending

**验收标准：**

- [ ] Evidence Bundle 关联输入、状态、截图、日志、Provider 和源 revision。
- [ ] Reviewer 分别判断静态、运行状态和运行视觉证据。
- [ ] 人类确认玩家目标是否成立，并记录相比直接使用 Codex + MCP 的实际收益与负担。

**验证：** 至少执行一次失败修复复验；旧证据不能用于新 revision。

**依赖：** Task 3.4。

## Checkpoint 3：使用场景 MVP 成立

- [ ] 从讨论到可运行 Godot 项目的完整链路可重复。
- [ ] 至少一个新素材完成生成、归一化、绑定和运行验证。
- [ ] 失败可以定位到讨论、查询、规格、素材、绑定、实现或证据之一。
- [ ] 人工确认框架确实减少了信息差，才进入 GameJam 真实制作。

## Phase 4：服务 GameJam 真实制作

每次只选择一个当前游戏功能作为纵切片：规格、实现、运行、证据、审核和修复必须
一起完成。具体功能与获奖策略由 TapTapGameJam 的项目 Plan 决定，不写入本计划。

首个纵切片必须是包含新增或修改素材的关卡/内容任务，以验证完整链路：

```text
Production Card -> Asset Spec -> Provider -> Godot Binding -> Runtime Evidence -> Human Verdict
```

框架侧每个纵切片只回答两个问题：

1. 现有框架是否让项目更快获得可信结果？
2. 这次产生的能力是否已经通用到值得晋升？

## Phase 5：晋升与回归

### Task 5.1：实现 Promotion Gate

项目候选经过静态检查、项目测试、运行重放、Reviewer、人工审批、去项目化、
许可证检查和框架回归后，才能进入稳定目录。

### Task 5.2：晋升 Production Contract

只把真实纵切片证明必要且稳定的 Production Card、Asset Spec 和 Godot Binding 字段晋升为
框架契约。引擎中立部分与 Godot 映射分层，删除项目名、路径、资产和 Provider 工具名。

### Task 5.3：建立框架回归基准

从真实项目缺陷中提取最小可公开重放的测试，参考 GameDevBench 和 GameCraft-Bench
的任务、轨迹和证据思想，但不复制项目专属内容。

## 风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 理论框架过度扩张、挤占 MVP 与 GameJam | 高 | 只实现三技能包和一条 MVP 所需合同；Checkpoint 1 人工收口 |
| MCP 候选不稳定 | 高 | 固定版本、契约隔离、保留 CLI 启动和诊断路径 |
| 项目代码过早进入框架 | 高 | Promotion Manifest + 证据 + 人工批准，缺一不可 |
| 两份文档再次混写 | 中 | 独立入口、仓库规则、跨仓链接而非复制正文 |
| 截图看似正确但状态错误 | 高 | 结构化状态、输入轨迹、信号和诊断与截图联合判定 |
| Agent 角色数量膨胀 | 中 | 保留最小逻辑职责；新增角色必须证明质量收益 |
| Production Model 成为第二套 SceneTree | 高 | 只保存任务增量与可丢弃查询；Godot 始终是真实源 |
| 素材生成成功被误判为内容完成 | 高 | 强制经过归一化、Binding、运行视觉与状态验证 |

## 当前开放问题

1. godot-ai 固定 revision 与当前 Godot 4.7.2 基线是否完全兼容？
2. 使用场景 MVP 是否明确只支持 GDScript，暂不覆盖 C#？
3. MVP 的小型游戏目标和最小玩家交互是什么？
4. 项目侧语义状态采用 Group、`_gamemaker_state()`，还是两者结合？
5. MVP Asset Spec 是否只覆盖一张 2D 静态或序列图素材？

这些问题会改变项目实现，必须在对应 Task 开始前由项目事实或人工决策确认。
