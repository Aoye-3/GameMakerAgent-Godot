# 框架与项目仓库边界

## 目标

GameMakerAgent 与 TapTapGameJam 是两个生命周期、发布节奏和事实来源都不同的
独立仓库。框架必须由项目实践推动，但不能与某一个项目绑定。

## 所有权

| 能力或制品 | GameMakerAgent | TapTapGameJam |
| --- | --- | --- |
| Agent 编排与角色协议 | 权威来源 | 选择版本并使用 |
| 跨引擎 Runtime Adapter 契约 | 权威来源 | 提供项目配置和验证场景 |
| Godot MCP 具体适配器 | 验证后维护 | 首次集成和实战反馈 |
| Evidence Bundle Schema | 权威来源 | 生成项目证据实例 |
| 通用 Skeleton、Module、Skill | 晋升后维护 | 项目内先产生候选版本 |
| 游戏代码、场景和资源 | 禁止保存 | 权威来源 |
| GDD、玩法和关卡设计 | 禁止保存 | 权威来源 |
| 项目排期、风险和复盘 | 只记录框架层影响 | 权威来源 |

## 依赖方向

TapTapGameJam 可以固定使用某个 GameMakerAgent 版本。GameMakerAgent 不得通过
相对路径、Git 子模块或硬编码仓库地址反向依赖 TapTapGameJam。

本机仓库路径属于本地配置，不得提交。仓库内可提交的关联信息只包含：

- 框架仓库标识和版本；
- Runtime Adapter 名称和版本；
- 项目侧语义观察约定；
- 证据输出位置；
- 已批准的能力晋升记录。

## 项目驱动的晋升流

```text
TapTapGameJam 项目问题
  -> 项目内最小实现
  -> 项目测试和运行证据
  -> 独立 Reviewer 审核
  -> 人工批准晋升
  -> 去项目化和许可证检查
  -> GameMakerAgent 契约测试
  -> 发布为框架能力
```

任何一步失败，候选能力继续留在项目仓库，不得以“以后补测试”为由提前进入框架。

## VibeGame 迁移边界

现有 VibeGame 是框架提炼来源，不是需要整仓复制的模板。迁移以能力纵切片进行：

1. 先定义目标契约和验收证据。
2. 从 VibeGame 找到满足该契约的最小实现。
3. 去除 Phaser、项目路径和上游仓库流程等非必要耦合。
4. 在 GameMakerAgent 独立验证。
5. 记录来源、差异和尚未迁移的行为。

## 文档边界

- 本文及 GameMakerAgent `docs/` 只讨论框架。
- TapTapGameJam `docs/project/` 只讨论具体游戏项目。
- 项目复盘可提出框架候选，但框架采纳结果必须在本仓库另行记录。
