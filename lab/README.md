# GameMakerAgent Framework Lab

`lab/` 是 GameMakerAgent V1 的框架本地实验区。它允许在 GameJam 项目开始前验证通用契约、
Skill、Godot 夹具和 Provider 适配，但不把实验结果提前描述为稳定框架能力。

## 边界

- 只保存去项目化的最小夹具和候选能力；
- 不复制完整 VibeGame、TapTapGameJam、godot-ai 或 GameStudio 仓库；
- 不保存具体游戏的玩法、关卡、剧情和生产资产；
- 外部来源必须记录 URL、revision、许可证、提取范围和改写内容；
- Godot 项目仍使用原生 `.godot`、`.tscn`、`.tres` 和 `.gd` 作为真实源；
- 候选通过框架回归后仍需真实游戏纵切片确认，才允许晋升为稳定能力。

## 当前内容

```text
lab/
├─ candidates/
│  └─ studio-advisor/       从项目候选迁入的低噪声顾问实验
├─ fixtures/
│  └─ godot-runtime-probe/  去项目化 Godot 运行与状态观察夹具
└─ sources/
   └─ upstreams.json        固定来源和许可证清单
```

## 运行

Godot 4.7.2 本地工具放在仓库 `.tools/godot/`，该目录被 Git 忽略。Windows 下执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-lab.ps1
```

测试入口会先验证候选 Eval JSON，再以 Godot 官方支持的 `--headless`、`--path`、`--script`
和 `--log-file` 参数运行 Godot 夹具。命令行参数依据：
[Godot command line tutorial](https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html)。
