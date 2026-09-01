# V1 框架来源迁入清单

## 状态

Snapshot，日期 2026-09-01。机器可读清单位于
[`lab/sources/upstreams.json`](../../lab/sources/upstreams.json)。

## 迁入原则

本轮采用“选择性迁入 + 去项目化”，不做整仓复制。文件只有满足以下条件才进入 Lab：

1. 能独立验证 GameMaker 的通用合同或低噪声边界；
2. 不包含具体玩法、关卡、剧情或生产资产；
3. 来源 revision 与许可证明确；
4. 目标路径明确标记为候选或夹具；
5. 能通过本仓库自己的测试入口执行。

## 已迁入制品

| 目标 | 来源 | 来源状态 | 许可证 | 改写 |
| --- | --- | --- | --- | --- |
| `lab/candidates/studio-advisor/` | `F:\.Vibegame\.vibegame\candidates\gamemaker-agent\` | 2026-09-01 本地未提交候选 | Apache-2.0 | 改变承载目录并规范 EOF；保持 Skill 和行为用例语义 |
| `lab/fixtures/godot-runtime-probe/` | TapTapGameJam runtime probe | `c4b7af6a4d854e800bee220247cf7ae9604d3378` | Apache-2.0 | 删除项目名称和项目目录假设；缩小窗口；增加 Group 与 contract version 断言 |
| `.tools/godot/` | 本地 Godot 4.7.2 stable | 本地二进制 | MIT | 不提交；增加 `_sc_` 进入 self-contained 模式 |

## 固定 Git 研究引用

核心参考实现以 remote-tracking ref 存在于 GameMakerAgent 的 Git 对象库中，不检出到工作树，
不参与发布，也不成为运行依赖。这样可以逐文件审查固定版本，同时避免整仓 vendor 和双份历史。

| 来源 | Research ref | Revision | 当前用途与状态 |
| --- | --- | --- | --- |
| VibeGame | `research/vibegame/main` | `7549e57105c6abf1848f714aea63762d540ce04f` | Task 1.0 已取证；只吸收资产关系、项目语义、运行与证据行为 |
| godot-ai | `research/godot-ai/main` | `a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e` | Task 1.0 已完成工具面映射；尚未安装或实现 Adapter，Phase 2 执行 conformance |
| Claude Code Game Studios | `research/claude-code-game-studios/main` | `984023ddac0d5e27624f2baacde6105e45de375f` | Task 1.0 已取证；专业知识压缩为字段、检查器和按需顾问参考 |
| GameStudio | `research/gamestudio/main` | `6027706e8923ba157a22a546c4c0be4b14b0ef4d` | Task 1.0 已与 CCGS 去重；只保留少量独有 2D 资产管线约束 |

逐文件来源、符号、目标形态、必要改写、许可证、拒绝项和去重证据见
[核心竞品源码吸收清单](core-source-intake.md)。该报告是 Task 1.0 的权威采用记录；早期横向
调研继续提供背景，但不再决定后续 Schema 或 Provider 范围。

`godot-ai` 的 Git ref 只证明源码已拉取和可复查。只有固定版本插件按官方方式安装到测试
Fixture、Adapter 实现完成并通过真实 Godot conformance 后，才能称为“已接入”。

## Godot 官方依据

- [`--headless`、`--path`、`--script`、`--log-file`](https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html)
- [Self-contained mode 与 `_sc_`](https://docs.godotengine.org/en/latest/tutorials/io/data_paths.html#self-contained-mode)

Godot 官方文档说明 self-contained mode 会把编辑器数据、设置和缓存写入可执行文件旁的
`editor_data/`。因此本地工具与其所有运行副产物都留在当前 F 盘工作区，不写入 C 盘用户目录。
