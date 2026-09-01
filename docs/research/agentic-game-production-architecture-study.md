# Agentic 游戏生产框架对比与 GameMaker 架构结论

## 调研范围

- **快照日期：** 2026-09-01
- **问题：** VibeGame 的统一生产语义如何与 Godot、通用编码 Agent、素材生成能力和现有
  MCP 协作；GameMakerAgent 应该补哪一层，而不是重复什么。
- **方法：** 对已拉取仓库读取固定 revision 的源码和说明；对其他项目读取官方仓库、
  公开架构与验证说明，并记录查询时 HEAD。未在本地执行的能力只视为项目声明。

## 固定来源

| 项目 | 本次来源 | Revision / HEAD | 许可证 | 验证深度 |
| --- | --- | --- | --- | --- |
| [VibeGame](https://github.com/Aoye-3/VibeGame) | 本地 Git 对象、Schema 与规范 | `7549e57105c6abf1848f714aea63762d540ce04f` | Apache-2.0 | 源码阅读 |
| [godot-ai](https://github.com/hi-godot/godot-ai) | 本地 Git 对象、工具与架构文档 | `a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e` | MIT | 源码阅读，项目实测待完成 |
| [Claude Code Game Studios](https://github.com/Aoye-3/Claude-Code-Game-Studio) | 本地 Git 对象、Agent、Skill、模板与 Hook | `984023ddac0d5e27624f2baacde6105e45de375f` | MIT | 源码阅读 |
| [GameStudio](https://github.com/bullish0x/GameStudio) | 官方仓库 | `6027706e8923ba157a22a546c4c0be4b14b0ef4d` | MIT | 文档阅读 |
| [Xenodot Forge](https://github.com/arthur0n/xenodot-forge) | 官方仓库 | `4c425b51ea9479a8690094b795001e3bbf86d3fc` | MIT | 文档阅读 |
| [Godot Gamestudio](https://github.com/schmoenraad/godot-gamestudio) | 官方仓库 | `9cab0e3b2ab3934e29d5735070657d78e91c253d` | Apache-2.0 | 文档与公开 pilot 阅读 |
| [Godogen](https://github.com/htdt/godogen) | 官方仓库 | `05cebffc8b10c5817e8a3db495b82e7b6004ab84` | MIT | 文档阅读 |
| [OpenGame](https://github.com/leigest519/OpenGame) | 官方仓库 | `7fb78d30874f92cdd6bad817cceaec1f9557dc49` | Apache-2.0 | 文档阅读 |

HEAD 只用于让结论可复查，不代表这些 revision 已通过 GameMaker 的本地兼容性或安全测试。

## VibeGame 真正值得保留的部分

本地源码显示，VibeGame 的价值不只在 Agent 分工。它用几组明确关系建立了生产语义：

- `project.json` 统一项目设置、入口场景、manifest 和输入；
- Scene JSON 拥有节点层级，Node 定义把视觉、碰撞、脚本、配置和子节点放在同一语义对象；
- `manifest.json` 用稳定资源键描述 image、spritesheet、atlas 和 tileset，原型占位图可以在不
  改引用的情况下替换；
- Sprite 规范把帧尺寸、序列、FPS、循环、Pivot、碰撞框和帧偏移连接起来；
- 资产清单和跨文件依赖显式化，减少设计、代码和素材各自命名的漂移。

这些关系直接服务于“设计一个新关卡”类请求：Agent 不只知道写代码，还能知道缺什么素材、
素材应以什么规格生产、如何成为场景对象以及怎么被玩法使用。

但原模型把 Scene/Node/Asset 语义与 Phaser 和自定义引擎共同固化。直接迁移到 Godot 会重复
Scene、Resource、Animation 和导入系统。因此应提炼**关系**，不复制其引擎数据模型：

| VibeGame 关系 | GameMaker 保留方式 | Godot 最终事实 |
| --- | --- | --- |
| 语义资源键 -> 文件 | Asset Spec 的稳定身份与来源 | `res://` 资源与引用 |
| 帧、FPS、循环 | Asset Spec + Godot Binding | `SpriteFrames` / `Animation` |
| Pivot、碰撞、帧偏移 | 绑定约束与验证点 | 节点 transform、shape、region |
| 节点视觉 + 脚本 + 配置 | 任务局部绑定计划 | `.tscn`、`.tres`、脚本 |
| 占位资产可替换 | 复用/替换计划与兼容检查 | 保持资源接口或显式迁移 |

## 竞品能力矩阵

`强` 表示该项目把该能力作为公开核心；`中` 表示部分覆盖或依赖人工约定；`弱` 表示不是
公开主轴。矩阵是架构判断，不是质量排行榜。

| 项目 | 项目语义 | 设计到内容 | 素材生产 | Godot 绑定 | 运行证据 | 低噪声/按需 | 人工晋升 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VibeGame | 强 | 强 | 中 | 弱，原生为 Phaser | 强 | 中 | 强 |
| godot-ai | 弱 | 弱 | 弱 | 强 | 强 | 中，依工具授权 | 弱 |
| Claude Code Game Studios | 强，文档型 | 强 | 强，规格型 | 中，角色建议 | 中 | 弱 | 弱 |
| bullish GameStudio | 强，文档型 | 强 | 强，技能覆盖广 | 中，多引擎指南 | 中 | 弱，55 Agent/182 Skill | 弱 |
| Godot Gamestudio | 中 | 中 | 中 | 强 | 强，revision/evidence 门禁 | 中，最小团队路由 | 弱 |
| Xenodot Forge | 中 | 中 | 中，共享资产库 | 强 | 强，确定性 Gate | 中 | 强，game-local -> plugin |
| Godogen | 中 | 强 | 强，多 Provider | 强 | 强，截图/视频自修复 | 强，当前强调薄指导 | 中，人工复盘 |
| OpenGame | 中，模板型 | 中 | 弱 | 不适用，Web | 强，Debug Skill | 强，双 Skill 核心 | 强，经验演化 |

## 各项目对 GameMaker 的实际启示

### godot-ai：执行面，不是产品语义层

godot-ai 已经覆盖广泛的场景、资源、脚本、运行、输入、截图、日志和自定义工具能力。它最
适合成为 Authoring / Runtime Provider。它不负责判断一张生成图为什么存在、应该采用什么
帧和 Pivot、如何满足关卡节奏，也不应承担跨 Provider 的公共契约。

**结论：** 配合使用；GameMaker 负责意图、Asset Spec、Godot Binding 和验收，godot-ai
负责执行。不要重写一套同规模 MCP 工具。

### Claude Code Game Studios / GameStudio：专业判断有价值，组织方式过重

固定 revision 中的 `art-bible`、`asset-spec`、`asset-audit`、Level Designer 和 Technical
Artist 已覆盖视觉规则、资产枚举、生成提示、尺寸、格式、性能预算、命名、复用和缺失引用。
这些知识证明“素材专业性”值得保留。

缺口也很明确：Asset Spec 主要产生 Markdown 和 manifest；Asset Audit 主要做文件、命名、
格式和引用扫描。它们没有形成稳定的“生成结果 -> 归一化 -> Godot Import -> Resource/
Scene Binding -> 运行证据”合同。大量问答阶段、Agent 交接和写入确认若常驻，会成为开发
噪声。

**结论：** 把专业知识压缩为三个形态：可选顾问视角、Asset Spec 字段、可执行检查器；
不复制组织图、阶段状态机和全量模板。

### Godot Gamestudio：最接近 Delivery Loop

它公开强调最小团队、职责不重叠、Maker/Reviewer 隔离、Godot QA、revision-bound review、
hashed evidence 和证据不足不能通过。其公开 pilot 明确只有 `n=1`，没有宣称普遍质量提升，
这一限制需要保留在比较中。

**结论：** 证据新鲜度、revision 绑定和 reviewer≠maker 应进入 GameMaker；它主要解决
“完成是否可信”，不是 GameMaker 要补的“素材怎样从意图进入 Godot”。

### Xenodot Forge：最接近项目孵化与人工晋升

它把框架与游戏分开，能力先 game-local，再由人类运行 promote 进入插件；验证使用共享
检查库和确定性 Gate。其说明同时承认 Godot headless 检查较浅、尚无深入玩法/行为测试，
并存在 Claude Agent SDK/API shape 倾向。

**结论：** 采用项目内生、人工晋升和生成器/审核器共享规则的思想；不采用 Web UI、Hive
拓扑和宿主绑定作为框架前提。

### Godogen：最接近端到端多模态制作

Godogen 能规划、写代码、调用多个素材 Provider、运行引擎并从截图或视频自修复。当前
仓库规则明确要求只提供模型难以快速推断的指导，避免明显知识污染上下文；这说明随着基础
Agent 变强，重型阶段技能可能反而成为负担。

它的素材链具有实际参考价值，但 Provider、C# 工程选择和发布生成器是具体实现，且公开
成果不能替代我们自己的可复现实测。

**结论：** 采用“画面证据驱动修复”“专业信息才进入上下文”和 Asset Provider 可组合的
思想；GameMaker 重点做稳定交接合同，而不是复刻一键生成器。

### OpenGame：模板和错误经验应分开演化

OpenGame 把核心 Game Skill 收敛为 Template Skill 与 Debug Skill：前者提供稳定起点，后者
积累经过验证的集成修复。这证明有效框架未必需要大量角色，结构知识和故障知识可以各自
演进。其目标是 Web 游戏，不能直接证明 Godot 资产绑定能力。

**结论：** GameMaker 的项目语义与验证故障库应分开；只有重复且验证过的经验才晋升。

## 评测给出的现实约束

- [GameDevBench](https://github.com/waynchi/gamedevbench) 的 Godot 任务显示，视觉反馈能改善
  结果，但最强系统仍远未解决全部任务，多模态任务尤其困难。
- [GameCraft-Bench](https://github.com/FreedomIntelligence/gamecraft-bench) 评估完整 Godot
  项目生成和可回放轨迹，但明确的自动检查仍不能代表主观“好玩”。

因此 GameMaker 的验证必须分层：静态、运行状态、运行视觉可以自动化；手感、创意质量和
是否达到玩家体验仍保留人类结论。框架不应伪造一个“fun score”。

## 客观定位与尚未证明的优势

现有项目已经分别覆盖了专业顾问、Godot 工具、多模态生成、运行验证和能力晋升。GameMaker
没有理由以 Agent 数量、技能数量、MCP 工具数量或“一句话生成游戏”竞争。

合理定位是：

> GameMakerAgent 是面向 Codex 等通用编码 Agent 的 Godot-first、Provider-neutral 游戏
> 生产语义与验证层；它把玩法意图、素材规格、Godot 绑定和可复核证据连接起来。

潜在差异是 `Production Bridge + Delivery Loop` 的组合：

```text
玩法设计
  -> 可实现内容规格
  -> 可生成素材规格
  -> Godot Resource / Scene 绑定
  -> 运行状态与画面证据
  -> 人工体验判断
```

这目前只是经过源码比较支持的架构假设，**还不是已验证的竞争优势**。只有真实关卡纵切片
证明它比“Codex + godot-ai + 生图工具直接开发”减少返工、遗漏或上下文噪声，才能成立。

## 建设结论

1. 保留 Studio Advisor，但让它只处理真正的创意取舍。
2. 紧接着验证 Production Bridge，不把 Asset Contract 推迟到项目后期。
3. 首个纵切片必须包含至少一个新素材及其 Godot 绑定，否则无法验证核心主张。
4. 复用 godot-ai 等现有执行 Provider；为替换和降级建立合同测试。
5. 把专业知识优先变成字段、检查器和查询规则；只有需要讨论时才成为 Skill。
6. 将运行证据绑定源 revision，视觉正确与状态正确分别判断，手感由人类裁定。
7. 任何框架能力先在具体项目验证，再通过来源、许可证、去项目化和回归门禁晋升。
