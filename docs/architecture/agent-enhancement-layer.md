# Agent 增强层与项目孵化路径

## 定位

GameMakerAgent 位于人类意图与具体游戏工具之间。它增强 Agent 的专业判断、任务协作、
统一生产语义、运行验证和经验复用，但不替代 Godot，也不把 godot-ai 或某个 MCP 变成
框架核心。

```text
Human intent
  -> Advisor: 讨论、质疑、取舍
  -> Production Bridge: 把决定翻译成内容、素材规格和 Godot 绑定
  -> Orchestrator: 把确认结果变成有验收标准的任务
  -> Maker: 修改原生游戏项目
  -> Runtime / Authoring Adapter: 调用 Godot、godot-ai 或其他 Provider
  -> Evidence: 输入、状态、截图、诊断和 revision
  -> Reviewer: pass / fail / insufficient_evidence
  -> Promotion: 把已验证能力提炼回 GameMakerAgent
```

## 保留的 VibeGame 精髓

- 用户原始目标和确认决定是上游事实，后续角色不能静默改写。
- 玩法、代码、场景和素材共享可追踪语义；Asset 的尺寸、帧、Pivot、碰撞提示和使用位置
  不能靠每个执行 Agent 临时猜测。
- Designer、Maker、Player、Reviewer 是职责边界；只有任务确实需要时才成为独立 Agent。
- “实现完成”必须经过真实运行、可回放输入、结构化状态、截图或诊断证据。
- Reviewer 与实现上下文保持判断独立，失败回到最小复现和新证据，而不是复用旧结论。
- 可复用知识通过真实项目验证和人工晋升积累，不进行无门禁的自动自我扩张。

不作为框架不变量的内容包括 Phaser 数据模型、固定团队人数、七阶段流程、tmux、Hook、
worktree、强制 GDD/模板以及第三方 MCP 工具名称。

Production Bridge 的详细边界见
[从玩法与素材意图到 Godot 可运行内容](production-bridge.md)。它只保存任务局部语义；原生
Godot 项目仍是 Scene、Resource、脚本和导入结果的唯一真实源。

## 两级目录

### 项目候选区

项目中的候选根固定为：

```text
.vibegame/candidates/gamemaker-agent/
```

按实际产生的能力创建子目录，不预建空骨架：

- `skills/`：顾问、复盘和其他可复用技能候选；
- `adapters/`：项目局部 Godot Provider 或工具适配候选；
- `evals/`：能复现价值或失败的最小场景；
- `promotion/`：准备晋升时的来源、证据和门禁记录。

游戏玩法、场景和资产仍留在项目原有目录，不复制到候选区。运行截图、日志等大体积证据
使用项目既有 evidence 位置，候选只保存可追踪标识。

### GameMakerAgent 稳定区

候选通过 Promotion Gate 后，去项目化版本进入 GameMakerAgent 对应的框架目录：

- `skills/`：可独立发现、按需加载的 Agent 能力；
- `adapters/`：Provider 无关端口和已验证实现；
- `contracts/` 或 `schemas/`：跨角色、跨引擎接口；
- `evals/`：不含私有项目内容的行为与契约回归。

目录只在首个通过门禁的制品出现时创建。GameMakerAgent 不通过本机相对路径读取项目候选。

## 首个垂直路径

1. 在项目候选区制作单入口 `studio-advisor`，先提供玩法、体验、范围和试玩复盘四个按需视角。
2. 顾问默认只讨论；用户确认后生成轻量 Decision Card，再交给编排层。
3. 从 VibeGame 提炼任务局部的 Production Card、Asset Spec 和 Godot Binding，不复制 Phaser
   Project/Scene/Node 模型。
4. 提炼最小 Orchestrator、Maker、Player、Reviewer 职责语义，不复制完整运行外壳。
5. 在项目中通过适配层实测 godot-ai 和 Asset Provider；失败时可以替换 Provider，而不改变
   上层生产语义。
6. 使用含新增素材的真实 Godot 纵切片验证“决定 -> 素材 -> 绑定 -> 实现 -> 运行 -> 证据
   -> 审核 -> 修复”。
7. 纵切片稳定后，把通用部分晋升到 GameMakerAgent，项目候选继续承担下一轮实验。

## 开发时的噪声边界

- Advisor 只在用户明确要求讨论、评估、比较或复盘时启用。
- 普通编码、修错和运行验证不加载顾问参考。
- Programmer 只接收确认后的决定和任务契约，不接收完整讨论记录。
- Production Bridge 按任务查询项目事实，不注入完整 GDD、Art Bible 或 SceneTree 镜像。
- Provider 错误被适配器归一化；不得把 MCP 说明书注入每个 Agent。
- 新角色或新技能必须能指出它减少了哪类错误、返工或证据缺口。
