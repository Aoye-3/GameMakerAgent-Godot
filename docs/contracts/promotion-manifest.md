# Promotion Manifest Contract

## 状态

Draft 0.1

## 目的

Promotion Manifest 记录一个项目局部能力为什么有资格进入 GameMakerAgent，防止把
GameJam 的偶然实现、私有资产或未经验证的代码包装成通用框架。

## 支持的候选类型

- `skill`
- `module`
- `skeleton`
- `contract`
- `adapter`
- `debug_recipe`
- `benchmark`

## 必填门禁

1. 项目问题和候选能力边界明确。
2. 来源仓库、revision 和原始路径可追踪。
3. 项目测试通过。
4. 真实运行重放通过并关联 Evidence Bundle。
5. 独立 Reviewer 通过。
6. 人工批准晋升。
7. 项目名称、绝对路径、玩法假设和私有资产已移除。
8. 依赖与许可证可进入框架。
9. 在 GameMakerAgent 中有独立验证或契约测试。
10. 目标目录和兼容性影响明确。

任一门禁为 `false` 时，状态不得为 `accepted`。

## 状态

- `candidate`：仍属于项目仓库。
- `reviewing`：正在去项目化和验证。
- `accepted`：已通过全部门禁，可以合入框架。
- `rejected`：不具备通用性或风险不可接受。
- `superseded`：已被更新版本替代。

机器可读草案见 [`schemas/promotion-manifest.schema.json`](../../schemas/promotion-manifest.schema.json)。
