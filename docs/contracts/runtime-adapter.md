# Runtime Adapter Contract

## 状态

Draft 0.1

## 目的

隔离 Agent 工作流与具体引擎、MCP Server、编辑器插件或 CLI。Player 和 Reviewer
只使用这里定义的语义，不直接依赖第三方工具名称。

## 最小操作

| 操作 | 语义 | 最小结果 |
| --- | --- | --- |
| `start` | 启动项目或指定场景并建立会话 | `session_id`、引擎版本、启动诊断 |
| `stop` | 停止会话并清理适配器创建的临时状态 | 清理状态和残留诊断 |
| `pause` | 在已定义的安全点冻结游戏 | 帧号或单调时间 |
| `resume` | 恢复自由运行 | 当前会话状态 |
| `input` | 注入命名动作、键盘、指针或定时序列 | 已接受的规范化输入轨迹 |
| `step` | 推进指定物理帧、渲染帧或时间 | 前后时间和实际推进量 |
| `step_until` | 推进至条件成立、超时或错误 | 条件结果及停止原因 |
| `observe` | 获取有界、允许列表内的语义状态 | 版本化状态摘要 |
| `capture` | 捕获与观察时刻关联的视口图像 | 文件标识、尺寸和时间戳 |
| `diagnostics` | 获取日志、解析/运行错误、信号和可选性能数据 | 游标和规范化条目 |

## 公共信封

每个调用必须携带：

- `contract_version`；
- `request_id`；
- `session_id`，`start` 除外；
- `operation`；
- `timeout_ms`；
- 操作参数。

每个结果必须返回：

- `request_id`；
- `status`: `ok`、`error`、`timeout`、`cancelled` 或 `unsupported`；
- 单调时间或帧定位信息；
- 规范化结果或错误；
- 可关联到 Evidence Bundle 的 artifact 标识。

## 时间语义

- 适配器必须声明 `step` 推进的是 physics、render 还是 wall-clock。
- `pause` 不能暗示音频、Tween、Timer 和异步导入全部被冻结；支持范围必须报告。
- `step_until` 必须有显式上限，禁止无界等待。
- 同一输入轨迹重复执行的差异必须能从证据中发现，不能静默忽略。

## 语义观察

`observe` 只返回项目显式公开的游戏语义。禁止默认转储完整 SceneTree。

候选约定包括：

- 节点加入 `gamemaker_watch` Group；
- 节点实现 `_gamemaker_state()`；
- 项目清单声明字段允许列表。

最终选择由 Phase 1 场景实测决定。无论选择哪种方式，输出都必须有版本、大小上限，
并排除密钥、任意文件内容和不相关节点。

## 错误模型

最小错误类别：

- `not_connected`
- `invalid_request`
- `unsupported_capability`
- `engine_start_failed`
- `engine_runtime_error`
- `observation_unavailable`
- `permission_denied`
- `timeout`
- `adapter_internal_error`

第三方 MCP 的原始错误可作为受限调试信息保留，但 Agent 决策使用规范化类别。

## 权限

观察与写入必须是不同能力。任意脚本、文件系统、网络、进程和场景状态修改默认拒绝，
只有项目策略显式允许时开放，并写入证据审计记录。
