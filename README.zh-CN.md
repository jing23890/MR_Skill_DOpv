# 概念 PV 制作 Skill

[English](README.md)

用 AI 编写场景、动画和合成代码，通过渲染器输出画面的概念 PV 工作流。目标是交付**可观看的视频和可修改的工程**，不依赖文生视频或文生图服务。

## 它解决什么问题

- 把主题拆成有叙事目的的镜头，避免把概念 PV 做成单一模型旋转展示。
- 根据镜头和图层分配工具，而不是把所有软件装一遍或强行只用一个软件。
- 指导程序化三维、相机、材质、动态光影、动态图形和声音的协作。
- 先检查风格帧与短动画，再做完整渲染；修改时复用未变化的结果。
- 检查逐帧输出、时间轴、编码、完整解码和可编辑源文件交付。

## 已验证与待扩展的边界

已经实践的流程是：

**Blender Python → Cycles/OptiX 光追 → 240 张 PNG → Pillow 逐帧绘图 → FFmpeg 合成 10 秒视频。**

实际样片为 1920×1080、24fps，使用 Blender 5.1.2、Windows 与 NVIDIA GPU。第二版加入移动窄光、冷暖交替、实体遮光片投影、透光核心与独立内部光源。

Remotion / Three.js、AE 和 UE 是本技能提供的选型与衔接建议，**没有将它们包装成已跑通的集成或现成插件**。使用这些路线时，需要在对应环境验证短片导出。

没有附带原样片、字体、软件安装包和第三方资源，避免把个人环境、特定视觉风格和额外授权混入公开技能包。

## 安装

把 `skills/concept-pv-production` 整个文件夹复制到你的 Agent 技能目录。

Codex 默认使用 `~/.codex/skills/`；若自定义了 `CODEX_HOME`，则使用该目录下的 `skills/`。其他支持 Agent Skills 的工具请按其文档选择目录。

本技能不要求连接 MCP，也不会自动安装所有候选软件。具体项目需要哪些工具，由 Agent 根据已有环境和制作需求判断。

## 使用示例

```text
使用 $concept-pv-production，制作一个 10 秒的原创深空观测站概念 PV。
用代码和渲染完成，避免单一模型展示；交付视频、原创音效和可编辑工程。
```

```text
使用 $concept-pv-production，保留这段视频的镜头，重新设计材质与光影。
让冷暖窄光交替扫过结构，增加真实移动阴影，避免核心整块泛白。
```

```text
使用 $concept-pv-production，做一支以字体和图形变换为主的 PV。
以 Remotion 管理时间轴，Blender 只负责两个重点三维镜头，先验证短片衔接。
```

## 包含哪些内容

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 触发条件、制作步骤、工具选型和按需阅读入口 |
| `references/blender-rendering.md` | 相机插值、节点版本差异、光追、色彩和断点续渲染 |
| `references/lighting-and-materials.md` | 平光、塑料感、过曝发光、移动阴影和材质层次 |
| `references/compositing-and-handoffs.md` | Blender、Remotion、Three.js、AE、UE 之间的职责与交接 |
| `references/delivery-and-validation.md` | 声音、序列帧、视频导出、验证与公开发布检查 |
| `assets/shot-plan.example.json` | 可修改的分镜与输出约定示例 |
| `scripts/encode_sequence.py` | 通用 PNG 序列编码和完整解码校验脚本 |

编码脚本只依赖 Python 3.10+ 标准库，以及带 `libx264` 的 FFmpeg。支持指定帧率、帧号、帧数和音频，拒绝缺帧、尺寸不一致和未明确允许的覆盖。通过解码检查后才保存最终 MP4，并输出 JSON 报告。详细命令见英文 README 或脚本 `--help`。

## 开源与贡献

使用 MIT 许可证，详见 [LICENSE](LICENSE)。许可证覆盖本包编写的内容；外部软件、字体、音乐和素材仍遵循各自授权。本项目与相关软件厂商无隶属关系。

欢迎贡献真实的工具衔接案例、版本兼容修正和短片验证结果。请区分“已经执行验证”与“设计建议”，并避免提交个人路径、凭据或无再分发授权的素材。

执行 `python -m unittest discover -s tests -v` 可运行 8 项编码器端到端检查。FFmpeg 不在 PATH 时，通过 `FFMPEG` 环境变量指定。没有 FFmpeg 时会跳过测试，跳过不代表验证通过。
