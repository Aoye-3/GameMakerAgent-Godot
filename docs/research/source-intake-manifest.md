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

## 只参考、不复制

| 来源 | Revision | 用途 |
| --- | --- | --- |
| VibeGame | `7549e57105c6abf1848f714aea63762d540ce04f` | 提炼资源身份、帧、Pivot、碰撞、输入和观察语义 |
| godot-ai | `a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e` | 后续 Authoring / Runtime Provider conformance |
| Claude Code Game Studios | `984023ddac0d5e27624f2baacde6105e45de375f` | 顾问与资产规格专业知识研究 |

## Godot 官方依据

- [`--headless`、`--path`、`--script`、`--log-file`](https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html)
- [Self-contained mode 与 `_sc_`](https://docs.godotengine.org/en/latest/tutorials/io/data_paths.html#self-contained-mode)

Godot 官方文档说明 self-contained mode 会把编辑器数据、设置和缓存写入可执行文件旁的
`editor_data/`。因此本地工具与其所有运行副产物都留在当前 F 盘工作区，不写入 C 盘用户目录。
