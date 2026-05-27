|   |   |   |
|:---:|:---:|:---:|
| ![preview](./info-craft-handmade-claude-managed-agents.jpeg) | ![preview](./info-craft-handmade-hermes-agent.jpeg) | ![preview](./info-craft-handmade-agent-runtime-orchestration.jpeg) |
| Claude Managed Agents | Hermes Agent | Agent Runtime Orchestration |
| ![preview](./info-craft-handmade-c4-banking-system.jpeg) | ![preview](./info-craft-handmade-agent-dev-pipeline.jpeg) | ![preview](./info-craft-handmade-opentelemetry-architecture.jpeg) |
| C4 Banking System | Agent Dev Pipeline | OpenTelemetry Architecture |

# 手绘知识图解模板(本批 6 个实例:技术架构图)

> 这是一个 **prompt 模板**(`【内容】` 段含占位符 `{请输入你的内容或者参考图片}`),用于把任意内容转成创意手帐 + 白板推演风格的知识图解。本批 6 张图主题各异(Claude Managed Agents / Hermes Agent / Runtime Orchestration / C4 Banking / Dev Pipeline / OpenTelemetry),共享本模板。
>
> 跨 trunk 共享形式:6 张图各有独立 trunk(`info-craft-handmade-<subject>`),都在 README 元数据 Prompt 列指向本模板文件。

<div class="prompt-head" id="prompt">Prompt 正文</div>

```text
请把我提供的内容转化成一张高可读性的手绘知识图解。风格像认真整理过的创意手帐 + 白板推演 + 咨询报告信息图,而不是冰冷模板。

【输出目标】
生成一张适合传播、汇报和复用的知识图解。它必须先让人抓住核心判断,再沿着模块逐步阅读,最后记住一句结论。

【语言要求】
图上所有可见文字根据用户的输入来确定语言,中文,英文或其他
不要混用语言,除非是技术名词、产品名、协议名、代码路径或数字指标。

【画布要求】
比例:{16:9 / 5:4 / 4:3 / 21:9}
质量:4K high resolution
背景:浅米白 / 浅暖灰,保留轻微纸张纹理和呼吸感。
整体清晰、留白稳定,不要把文字挤到看不清。

【信息设计规则】
不要逐字搬运原文。先压缩信息,再画图。
请把内容整理成:
1. 顶部:强标题 + 一句话核心判断
2. 中部:3-6 个主模块,按流程、对比、阶段或因果关系排列
3. 模块内:每个模块最多 3-5 条短 bullet
4. 底部:一条 Flow Summary / Decision Summary / Bottom Line
5. 如果内容很多,只保留最关键的 8-10 个判断,避免微型文字

【可读性规则】
标题必须最大、清楚、有重量。
模块标题要有秩序,正文必须短句化。
每个模块不要超过 6 行正文。
每条 bullet 尽量简短。
不要使用密密麻麻的小字表格。
不要为了完整而牺牲可读性。

【视觉风格】
黑色或深墨色手写线条建立阅读骨架。
使用圆角分区、细线框、轻阴影、编号、箭头、标签和小图标。
线条允许轻微手绘抖动,但整体对齐、边距、分组要稳定。
图标只做路标和强调,不要抢走文字层级。

【配色规则】
使用克制的标记笔色彩:
浅米白背景 + 黑色主线条;
低饱和青绿、鼠尾草绿、淡紫、柔橙、浅蓝作为分区和路径颜色。
避免霓虹色、强渐变、过度商业光效和整页单色化。
彩色区域只占少量到中等面积。

【准确性规则】
严格保持输入内容中的技术链路、组件名称、箭头方向、协议、端口、数据流和判断。
不要自行新增未提供的组件。
不要把动作写错,例如「读取日志」不能画成「生成日志」。
如果空间不足,优先保留主链路、关键差异和最终判断,删掉次要解释。

【内容】
{请输入你的内容或者参考图片}
```
