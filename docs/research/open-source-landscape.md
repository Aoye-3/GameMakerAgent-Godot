# 相似开源项目与采用建议

## 状态

Research snapshot，最近复核日期 2026-09-01。仓库活跃度、接口和版本会变化；所有候选在
成为依赖前必须以固定版本完成本地实测。

本页保留候选清单；统一生产语义、资产到 Godot 的信息差和详细能力矩阵见
[Agentic 游戏生产框架对比与 GameMaker 架构结论](agentic-game-production-architecture-study.md)。

## 框架和晋升模式

| 项目 | 借鉴内容 | 不直接采用的原因 |
| --- | --- | --- |
| [Xenodot Forge](https://github.com/arthur0n/xenodot-forge) | 框架与 Godot 游戏分仓、项目局部能力晋升框架 | 仍是 POC，接口不稳定 |
| [GodoGen](https://github.com/htdt/godogen) | 分阶段制作、运行引擎、用证据替代完成声明 | 完整流程较重，不能阻塞 GameJam 迭代 |
| [OpenGame](https://github.com/leigest519/OpenGame) | Template Skill 与 Debug Skill 分开演化 | 主要面向 Web 游戏，不提供 Godot 运行层 |
| [Godot Gamestudio](https://github.com/schmoenraad/godot-gamestudio) | Maker/Reviewer 分离、证据新鲜度门禁 | 早期项目，公开验证样本有限 |
| [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | 游戏设计、范围控制和复盘的专业判断框架 | 大量 Agent、阶段门禁和模板会使日常开发过重 |
| [GameStudio](https://github.com/bullish0x/GameStudio) | 多引擎专业知识、资产规格、技术美术与团队协作覆盖 | 55 Agent / 182 Skill 的宽度不是首版目标，常驻会增加上下文噪声 |

## Godot 控制和运行验证

| 项目 | 候选价值 | 当前决定 |
| --- | --- | --- |
| [hi-godot/godot-ai](https://github.com/hi-godot/godot-ai) | 广泛编辑能力、运行输入、截图、日志和项目自定义工具 | Phase 2 首测 Provider；固定版本并通过 Adapter 限权 |
| [satelliteoflove/godot-mcp](https://github.com/satelliteoflove/godot-mcp) | 冻结、推进、输入、结构化状态、截图和诊断与 VibeGame RuntimeBridge 接近 | godot-ai 确有运行阻断缺口时的对照候选 |
| [Erodenn/godot-mcp-runtime](https://github.com/Erodenn/godot-mcp-runtime) | 临时运行桥、较低项目侵入、headless 工作流 | headless 或项目侵入失败时的回退候选 |
| [Vollkorn-Games/godot-mcp](https://github.com/Vollkorn-Games/godot-mcp) | 批量输入、信号同步、状态检查点和只读工具策略 | 借鉴模式；项目较新，暂不作为依赖 |

GameMaker 采用 MCP 的架构依据是“聚焦、可组合的服务器”，而不是单一全能 Server。
参考 [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)。

Godot 原生扩展和调试边界以官方文档为准：

- [EditorPlugin](https://docs.godotengine.org/en/stable/classes/class_editorplugin.html)
- [EngineDebugger](https://docs.godotengine.org/en/stable/classes/class_enginedebugger.html)
- [EditorDebuggerPlugin](https://docs.godotengine.org/en/stable/classes/class_editordebuggerplugin.html)
- [Command line tutorial](https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html)

## 测试和回归

- [GdUnit4](https://github.com/godot-gdunit-labs/gdUnit4)：首选白盒单元、场景、输入和信号测试候选。
- [GUT](https://github.com/bitwes/Gut)：成熟备选；首版不同时引入两套测试框架。
- [GameDevBench](https://github.com/waynchi/gamedevbench)：参考 Godot 编码任务和视觉反馈评测。
- [GameCraft-Bench](https://github.com/FreedomIntelligence/gamecraft-bench)：参考完整项目、可回放轨迹和验证器设计。

## 当前采用结论

1. 采用 Xenodot Forge 的“双仓 + 项目内生 + 晋升”思想，不采用其实现作为底座。
2. 保留 VibeGame 的统一生产语义与 Agent/证据闭环，提炼 Production Bridge 和交付契约，
   不复制整个 Phaser 引擎。
3. 先用同一项目场景实测固定版本 godot-ai；存在阻断缺口时再用相同矩阵比较其他 MCP。
4. 以 GdUnit4 白盒测试补充 MCP 黑盒运行证据。
5. 首版把角色保留为最小职责链，不复制大型角色目录或强制阶段状态机。
6. 把生图等能力视为 Asset Provider；素材只有在完成归一化、Godot Binding 和运行验证后
   才算可用。

以上均为采用方向，不代表候选已经通过 Windows、目标 Godot 版本或 TapTapGameJam
实际场景验证。
