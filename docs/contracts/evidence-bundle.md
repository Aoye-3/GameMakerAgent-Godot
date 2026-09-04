# Evidence Bundle Contract

## 状态

Draft 0.1

## 目的

Evidence Bundle 把“Agent 说已经完成”转化为可重放、可定位到源版本的验证事实。
截图只是其中一种制品，不能单独证明玩法正确。

## 必填信息

- 唯一 `evidence_id` 和 Schema 版本；
- 项目仓库标识、实现 ID、内容指纹；ProjectContext 同时保留 Git revision；
- Provider 身份/版本、session ID、run ID，不能为旧证据补造；
- GameMaker、Runtime Adapter、Godot 和 MCP 版本；
- 测试场景与验证目标；
- 初始条件和规范化输入轨迹；
- 运行前后语义状态及断言结果；
- 当前 V1 视觉纵切片的运行截图，以及每个制品的路径与 SHA-256；
- 本次会话的错误与警告摘要；
- 开始、结束时间和运行时定位；
- 证据产生者及 Reviewer 结论。

## 新鲜度规则

以下任一情况会使证据失效：

- 证据 revision 与被审核代码不一致；
- 截图和状态来自不同会话或无法关联到同一时间点；
- 输入轨迹缺失或无法重放；
- 引擎或适配器版本缺失；
- Reviewer 无法区分未运行与运行成功。

## Reviewer 结论

- `pass`：目标断言成立、没有阻断诊断、证据完整。
- `fail`：运行完成但目标断言失败，或存在阻断错误。
- `insufficient_evidence`：证据缺失、过期、来源不一致或不可重放。

机器可读草案见 [`schemas/evidence-bundle.schema.json`](../../schemas/evidence-bundle.schema.json)。

当前入口为 `gamemaker evidence review --project <path> --work <id>`：读取真实项目、当前源码 /
PNG / 导入配置指纹、Production、Normalized Asset、Binding 节点和资源引用，再验证证据哈希。
旧 `--input` 文件模式仅辅助诊断，不能返回 PASS。索引可重建，Dock 还会检查源码与记录哈希，
不会把旧索引的 PASS 当成当前事实。记录为纯本地证据，不是防恶意伪造的远程签名认证。
