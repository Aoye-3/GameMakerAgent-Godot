# 框架契约

框架契约稳定 Agent、引擎适配器和项目之间的协作语义。它们不承诺某个 MCP 的
工具名称，也不重新定义 Godot 的场景和资源模型。

| 契约 | 状态 | 用途 |
| --- | --- | --- |
| [Runtime Adapter](runtime-adapter.md) | Draft 0.1 | 统一运行、输入、推进、观察和诊断 |
| [Evidence Bundle](evidence-bundle.md) | Draft 0.1 | 保存可关联、可复现的验证证据 |
| [Promotion Manifest](promotion-manifest.md) | Draft 0.1 | 控制项目候选能力进入框架 |

机器可读草案：

- [`schemas/evidence-bundle.schema.json`](../../schemas/evidence-bundle.schema.json)
- [`schemas/promotion-manifest.schema.json`](../../schemas/promotion-manifest.schema.json)

契约在 Phase 1 实测前保持 Draft。第一次真实 Godot 纵切片通过后，才允许提升为
Accepted 1.0；版本提升必须说明兼容性。
