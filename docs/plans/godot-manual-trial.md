# 里程碑：可亲自使用的 Codex + Godot + MCP 开发闭环

状态：Active / 内部试用候选；承接 ADR-007，不代表 0.1.0 发布。

## 用户结果与边界

用户打开 Godot 和 Codex，用自然语言完成单场景四方向移动与收集；一张生成的 64×64 RGBA
角色素材进入真实节点。接触目标后 items_collected 从 0 变为 1、目标消失。随后把速度提高
20%，在同一个项目中增量修改、重新测试，并在只读 Dock 查看目标、实现和新鲜证据。

Codex 编排，成熟 MCP 执行，Godot 文件是真相。不增加 Runtime、MCP 产品或 Skill 数量。
代码、依赖、缓存、Godot 用户数据和产物留在当前 F 盘工作区；原地分支，禁止 worktree。

## 执行清单与门禁

1. **准备与真实连接（进行中）。** 用户在原生 Project Manager 创建
   `Project1/project-1`（用户已创建，替代最初建议的 lab 路径），Godot 4.7.2、Compatibility、GDScript。
   安装固定 godot-ai 3.2.4 revision a468a7eedd7dcbbeb0221a297f7e7c50f5ab2b4e 的外部组件、
   GameMaker Dock 与工作区 Skills；项目级 attach 配置不覆盖全局服务。关闭遥测及自动升级。
   核对目标绝对路径、端口和会话，不结束其他进程。
   **A：Codex 实际调用 MCP 并读到目标编辑器状态，配置存在不算通过。**
2. **Core 修复（待完成）。** 真实输入映射和 UID 入口；排除第三方源码干扰；Decision JSON
   真相与 Markdown 摘要统一；Normalized Asset 可校验、记录和编译；Evidence 实现引用与
   Schema 一致；Git revision 与源码/PNG/导入设置指纹同时记录。审核当前项目，检查
   Production、Binding、实现、证据闭合；空断言、缺图、错节点和过期内容不得 PASS。
   **B：两个假 Provider 通过同一 Schema/CLI/记录链的成功、超时、能力不足、运行失败、
   素材失败与证据过期矩阵，而不是只解析用例文件。**
3. **真实能力矩阵（待完成）。** MCP 编辑场景/脚本/Resource/输入、导入、启动、输入、
   观察、截图、诊断、停止；记录版本、项目、session/run 与错误。连续两轮无重复状态，
   重启编辑器后验证重连。不把时间线输入说成确定性步进。
   **C：真实矩阵通过才称 Provider 已接入，不用 CLI 代跑冒充 MCP 成功。**
4. **素材与玩法（待完成）。** 成熟图片 Provider 生成，归一化并记录来源/处理/许可；
   本轮单帧、居中 Pivot、不 trim。检查实际透明度与可见内容，拒绝空白图和实心背景。
   通过检查后才由 MCP 导入绑定；替换时保持稳定 ID 和目标路径。
   **D：目标、素材、节点、实现与运行截图可双向追踪，玩法实际可操作。**
5. **试用交付（待完成）。** Dock 只读展示目标、风格、素材、实现、Provider、审核和新鲜度；
   doctor 区分本地准备、实时连接、真实 conformance。提供准备/启动入口、中文步骤和
   制作、修改速度、复验三条提示词；同步权威计划与 README 状态。

## 最小接口与兼容

- doctor 始终只读：`files_ready` 仅为本地检查，`provider_connected` 和
  `conformance_passed` 未验证时为 null，不能以它们推断 ready。实时探测不启动游戏或写场景。
- 增加 CLI 素材检查/归一化与 Normalized Asset 合同；按 project + work_id 审核真实记录。
- Evidence 必须关联实现、运行身份与制品哈希；旧记录可读，但字段不足不能自动升级 PASS。
- Provider 声明能力与实测结果分离；公共卡片不含具体 MCP 工具名。

## 正式交付要求

全部回归通过；真实 MCP 两轮和重连通过；首次玩法及速度 +20% 修改均产生新证据；修改
PNG/脚本使旧证据失效；不合规素材阻断导入；Dock 加载刷新前后项目内容哈希不变（排除引擎
缓存）。用户不必填写 JSON 或手动接线，只需打开已准备环境、输入需求和试玩。

图片 Provider 不可用、MCP 未加载或证据缺失均是阻塞，不降低门禁。首次空项目创建、信任、
插件启用及 MCP 重载确认由用户完成。正式验收仍用同一项目；最终价值由用户判断。

## 2026-09-04 实施记录

- 已复现并修复 doctor 把仓库 Dock 误当作目标项目已安装、以及静态检查误报整套环境 ready。
- 用户已创建 Project1/project-1；A/C/D 和完整试用交付尚未通过，不能宣称已连接或已可试玩。
