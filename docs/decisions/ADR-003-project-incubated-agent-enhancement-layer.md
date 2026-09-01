# ADR-003：在项目 `.vibegame` 中孵化 Agent 增强层，再晋升到 GameMakerAgent

## 状态

Accepted

## 日期

2026-09-01

## 背景

VibeGame 已经证明了用户目标、专业职责、任务交接、运行证据和独立审核组合起来的价值，
但其公开实现同时绑定了 Phaser 项目模型、固定团队拓扑、运行 Hook 和较重的模板流程。
Game Studios 提供了有价值的专业游戏设计判断，但直接采用其多 Agent、阶段门禁和文档模板
会给日常开发增加上下文噪声。

Godot 能通过 godot-ai 或其他 MCP 获得编辑器和运行时能力，但这些项目会变化，也不应决定
GameMakerAgent 的角色、提示词或公共接口。框架需要先形成独立的 Agent 增强层，再让具体
引擎和工具作为可替换执行端接入。

## 决策

1. GameMakerAgent 的核心产品是**引擎中立、工具中立的 Agent 增强层**，不是新的游戏引擎，
   也不是某个 MCP 的包装器。
2. 新能力先在具体项目的 `.vibegame/candidates/gamemaker-agent/` 中孵化。首个候选是轻量
   `studio-advisor` 顾问层，后续才按真实需求增加编排、适配器或评估候选。
3. 从 VibeGame 保留的是语义能力：用户意图优先、职责隔离、任务交接、真实运行证据、独立
   审核和经验证能力晋升；不要求保留 Phaser、固定 Agent 数量、tmux、Hook、worktree 或
   强制模板。
4. Godot、godot-ai 和其他 MCP 位于 Runtime Adapter / Authoring Adapter 之后。Agent 只依赖
   GameMaker 语义，不依赖第三方工具名称。
5. 候选通过项目验证、Reviewer、人工批准、去项目化和许可证检查后，完整通用版本进入
   GameMakerAgent 自己的 `skills/`、`adapters/`、`contracts/`、`evals/` 等框架目录。
6. 项目候选与框架稳定版本不做持续双向同步；只在一个可验证纵切片结束时评估一次晋升。

“引擎中立”的产品范围由
[ADR-004](ADR-004-production-bridge-and-godot-native-source-of-truth.md) 进一步澄清为
Godot-first、Provider-neutral：公共语义不绑定具体 MCP，但不构建跨引擎最低公分母模型。

GameJam 前的开发顺序由
[ADR-005](ADR-005-framework-local-lab-before-game-project.md) 部分修订：去项目化通用底座可以
先进入框架 `lab/` 测试，但仍需真实项目纵切片才能晋升为稳定能力。

## 备选方案

### 直接修改并长期维护 VibeGame 上游实现

会继续继承 Phaser 项目模型和既有运行组织，难以形成真正的引擎中立增强层，拒绝。

### 直接把 Game Studios 的 Skills 和 Agents 复制到框架

专业知识有价值，但原组织方式过重，且会让顾问参与普通实现上下文，拒绝。

### 直接围绕 godot-ai 构建 GameMakerAgent

可以更快获得工具数量，但会把框架生命周期绑定到单一提供者，拒绝。godot-ai 只作为首个
Godot 候选 Provider。

## 后果

- `.vibegame/candidates/gamemaker-agent/` 是项目候选区，不是框架发布目录。
- GameMakerAgent 可以逐步替换 Godot Provider，而不重写顾问、编排和审核语义。
- 首版优先验证少量高价值能力，不以 Agent 数量、技能数量或 MCP 工具数量衡量完整度。
- 项目局部实现可能与最终框架实现不同；晋升时必须重写项目路径和玩法假设。
