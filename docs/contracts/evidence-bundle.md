# Evidence Bundle Contract

## 状态

Draft 0.1

## 目的

Evidence Bundle 把“Agent 说已经完成”转化为可重放、可定位到源版本的验证事实。
截图只是其中一种制品，不能单独证明玩法正确。

## 必填信息

- 唯一 `evidence_id` 和 Schema 版本；
- 项目仓库标识与 Git revision；
- GameMaker、Runtime Adapter、Godot 和 MCP 版本；
- 测试场景与验证目标；
- 初始条件和规范化输入轨迹；
- 运行前后语义状态及断言结果；
- 决定性截图或明确说明该验证不需要截图；
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
