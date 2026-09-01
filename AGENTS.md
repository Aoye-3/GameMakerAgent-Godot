# GameMakerAgent Working Rules

## Repository Role

本仓库是可迁移、可复用的游戏开发框架，不是具体游戏项目。

- 框架技术文档只写入 `docs/`。
- 不把 TapTapGameJam 的玩法、关卡、剧情、排期和游戏资产写入本仓库。
- 新能力默认先在具体项目中验证，达到晋升门禁后再提炼到本仓库。
- 项目侧 GameMakerAgent 候选统一在 `.vibegame/candidates/gamemaker-agent/` 孵化；本仓库只接收
  通过门禁后的去项目化版本。
- 提炼时必须移除项目专属路径、资产、名称和未授权依赖，并保留来源和许可证记录。
- Godot、Phaser 或其他引擎实现必须位于可替换适配器之后；不要让 Agent 角色依赖某个 MCP 的工具名称。

## Documentation Contract

- `docs/architecture/` 描述已经成立的框架边界。
- `docs/contracts/` 描述跨角色、跨引擎的稳定接口。
- `docs/decisions/` 记录代价高、难以逆转的架构决策。
- `docs/plans/` 记录未来工作、验收标准和实际状态。
- `docs/research/` 保存有来源、会随时间变化的技术调研。
- 架构改变时，在同一变更中更新相关文档。

具体 Godot 项目文档在独立的 TapTapGameJam 仓库维护。两个 Doc 体系不混写。
