# CLAUDE.md · Image Seed 项目工作指南

个人 AI 生图参考/灵感库。非代码项目,Markdown 是主要展示方式。图片按「场景 × 风格/布局」两层结构组织,分类体系对齐 [baoyu-skills](https://github.com/JimLiu/baoyu-skills)。

## 目录结构

```
image-seed/
├── README.md                    # 总导航(场景表 + 精选墙)
├── CONTRIBUTING.md              # 新增/归类图片 checklist + 命名规范
├── CLAUDE.md                    # 本文件
├── .gitignore
├── <scenario>/                  # 场景目录
│   ├── README.md                # 场景画廊(3 列平铺,每图一格)
│   ├── <substyle>/              # 子分类(有图才建,适用于细分场景)
│   │   ├── README.md            # 子分类画廊 + 元数据表
│   │   └── *.webp/jpg/png
│   └── *.webp/jpg/png           # 扁平场景直接放图(无 substyle 时)
├── unclassified/                # 图片待归类缓冲(场景类)
└── scripts/
    ├── gen_scenario_readmes.py  # 图片增删后必跑(仅对带 styles/layouts 的场景)
    └── pull_baoyu.sh            # baoyu-skills 更新时重跑
```

## 场景与缩写

| 场景目录 | 文件名前缀 | 结构 |
|---|---|---|
| `xhs-images/` | `xhs` | 9 styles + 6 layouts |
| `infographic/` | `info` | 17 styles + 20 layouts |
| `comic/` | `comic` | 6 layouts |
| `slide-deck/` | `deck` | 16 styles |
| `article-illustrator/` | `art` | 8 styles |
| `poster/` | `poster` | 扁平(有图才建子分类) |
| `ecommerce/` | `ecommerce` | 扁平 |
| `seasonal/` | `seasonal` | 扁平 |
| `travel/` | `travel` | 扁平 |
| `app-ui/` | `appui` | 扁平 |
| `anime/` | `anime` | 扁平 |
| `product-design/` | `prod` | 扁平 |
| `unclassified/` | `misc` | 暂存区,处理完清空 |

带 styles/layouts 的 5 个场景由 `scripts/gen_scenario_readmes.py` 自动生成 README;7 个扁平场景的 README 手动维护(画廊 + 元数据表合一)。

## 文件命名规则

格式:`<scenario-prefix>-[<substyle>-]<subject>-<modifier>[-nn].<ext>`

- 仅 `a-z 0-9 -`,全小写连字符;总长 ≤ 70 字符
- 不用 `copy`/`new`/`final`/`v2` 等噪声词
- baoyu 官方示例统一后缀:`<prefix>-<substyle>-baoyu.webp`(下载脚本按此模式)
- 本地收藏图用语义化名:如 `deck-sketch-notes-how-ai-learns.jpg`
- 扁平场景没有 substyle 段,直接 `<scenario-prefix>-<subject>.<ext>`,如 `poster-mortal-cultivation.png`

## 场景 README 布局规则(重要约束)

带 styles/layouts 的 5 个场景:**3 列平铺大网格,每张图占一格。** 参考基准:baoyu-skills 的 README 风格,以及当前的 `infographic/README.md`。

核心规则:
1. **平铺结构**:一个大 3 列 Markdown 表格,所有子分类的所有图全在这一个表格里
2. **一张图一格**:子分类有 N 张图就占 N 个格子,同子分类的图**连续相邻排列**(相邻同标签 = 同组)
3. **本地图优先**:同一子分类下,非 baoyu 图排前,`-baoyu.webp` 排后
4. **缩略图尺寸**:不用 HTML `<img width>` 控制 — 依靠 markdown 3 列表格列宽自动均分,**前提是每行 3 格至少有 2 格有图**(否则空列坍缩导致残图被拉大)。当前实现因为平铺连续,天然满足
5. **不使用 H3 小节分段**:用户明确反馈分段式展开会让单张图占满列宽"太大",必须平铺
6. **点击行为**:缩略图和文字标签都跳转到 **子分类 README**(不跳图片,不跳目录)

运行 `python3 scripts/gen_scenario_readmes.py` 自动按以上规则重生成 5 个场景 README。

扁平场景(7 个新场景)的 README 等价于一个"放大版的子分类 README":**画廊 + 元数据表**,两块都手维护。布局规则与下方「子分类 README 布局规则」相同。

## 子分类 README 布局规则

两个区块,**画廊**和**元数据**分离(合并会让表格过宽):

```markdown
## 画廊
|   |   |   |
|:---:|:---:|:---:|
| [![filename](./filename.ext)](./filename.ext) | ... | ... |
| `short-label` | ... | ... |

## 元数据
| 文件 | 主体 | 标签 | 来源 | Prompt |
|---|---|---|---|---|
| [filename](./filename.ext) | 描述 | `tag1` `tag2` | [source](...) 或 — | `prompt` 或 — |
```

- 画廊的图片链接指向图片文件本身(点击看原图)
- 元数据表的文件名列也是链接,缺失信息填 `—`,标签用反引号包裹

## 链接规范(踩过的坑)

**所有指向目录的链接必须显式写到 `/README.md`,不能裸目录结尾**。

| 写法 | GitHub | 本地预览 | 结论 |
|---|---|---|---|
| `](./xhs-images/)` | 能打开 | 不可点击 | ✗ 不用 |
| `](./xhs-images/README.md)` | 能打开 | 能点击 | ✓ 统一用这个 |

场景内指向子分类同理:`](./cute/README.md)`。场景内指向图片用 `](./cute/file.jpg)`(图片就是文件不用改)。

## 去重规则(踩过的坑)

**下载外部图库前、或首次处理用户上传图时,必须做去重检查。**

### 强信号(零成本判断)

- **文件名匹配 substyle 名**:若用户上传的原始文件名等于某 substyle(如 `sketch-notes.jpg` = `slide-deck-styles/sketch-notes`),高度可能**就是**该图库的官方示例本身。当即标记怀疑。
- **文件名含图库标识**:含 `baoyu`、`midjourney-showcase` 等词时同理。

### 视觉对比(当强信号触发时)

格式不同(jpg ↔ webp)无法用 hash,用 Read 工具读取成对图片逐张视觉对比。**注意:并行读取多张图时输出与调用顺序不一定 1:1 对应**,见下方「图片归类(踩过的坑)」。

### 处理方式(确认重复后)

1. 保留**语义更具体的文件名版本**(如 `deck-sketch-notes-how-ai-learns.jpg` > `deck-sketch-notes-baoyu.webp`)
2. 删除冗余版本
3. 在子分类 README 元数据表注明 `来源: [baoyu-skills](...)`,标签加 `` `baoyu-skills` ``
4. 跑 `scripts/gen_scenario_readmes.py` 更新场景网格
5. 更新根 README 场景导航表的「现有图片」数字

## 图片归类(踩过的坑)

**并行 Read 多张图时,输出和调用顺序不一定 1:1 对应**,会导致内容与文件名对应错位、mv 后归类错乱。

处理待归类图片时:
- 优先**单图独读**判断内容,确认后再 mv
- 若并行读取,必须用文件大小/格式做交叉验证(如 jpeg 通常远小于 png),不能仅凭视觉印象按调用顺序对应
- mv 完成后,**至少抽读关键文件单独验证一次**(尤其新建子分类、文件名含强语义信息时)

## 标签约定

- 全小写、连字符、1–2 词:`warm` `rain` `cel-shading` `low-light` `pastel`
- 优先复用已有标签,避免 `dark`/`darkness`/`night-dark` 并存
- 仅在元数据表中用,反引号包裹(`` `rain` ``);便于 GitHub 仓库搜索跨场景命中
- **模型来源**也用标签记录:GPT Image 2 生成的图打 `` `gpt-image-2` `` 标签。未来增加 midjourney/flux/gemini 时同理(`` `midjourney` `` 等)

## 新增/修改图片后必须更新的地方

见 CONTRIBUTING.md 的 checklist,核心:

1. 子分类 README(或扁平场景 README)的画廊和元数据表(手改)
2. 跑 `python3 scripts/gen_scenario_readmes.py`(自动更新 5 个非扁平场景 README 的平铺网格)
3. 根 README 的场景导航表数字(手改)

## 常用脚本

### `scripts/gen_scenario_readmes.py`

扫描各子分类目录下的实际图片文件,重新生成 5 个非扁平场景 README(`xhs-images`、`infographic`、`comic`、`slide-deck`、`article-illustrator`)。**图片任何增删后都要跑**。核心逻辑:

- 按子分类顺序遍历,每张图一个 tile
- 本地图排前、baoyu 排后
- 输出 3 列 Markdown 表格,相邻同子分类标签=同组

7 个扁平场景的 README **不由脚本生成**,手动维护。

### `scripts/pull_baoyu.sh`

从 baoyu-skills 仓库拉取全部 82 张示例图到本地对应子分类目录(带 `-baoyu.webp` 后缀)。仅在 baoyu-skills 更新、需要重新同步时运行。

**跑完必须对照去重清单手动删除已知重复项**(见脚本头注释)。

## 关键历史决策备忘

- **两层结构**:场景 → 子分类。不嵌 `styles/`/`layouts/` 子目录,扁平更直接。
- **子分类目录按需创建**:不预建空目录;有图才建,场景 README 的「可用子分类」清单作为"词典"引导。
- **无独立标签索引文件**:<200 张规模下,同步索引必然过期,改用「元数据反引号标签 + GitHub 搜索」。
- **不强制 webp**:GitHub 对 jpg/png 渲染更稳,单图 < 1MB 即可,格式混用无妨。
- **2026-05 废弃 gpt-image-2 顶层目录**:原先曾用 `gpt-image-2/` 作为「按生成模型来源」的正交维度,实践发现与场景体系并行维护两套数字增加负担、且粒度对不齐。统一回归单一场景维度:7 个原 gpt-image-2 子分类(`poster`/`ecommerce`/`seasonal`/`travel`/`app-ui`/`anime`/`product-design`)升格为顶层扁平场景;`gpt-image-2/infographic` 17 张并入 `infographic/` 各 styles/layouts;`gpt-image-2/xhs` 3 张并入 `xhs-images/` 各 styles/layouts;模型来源以 `` `gpt-image-2` `` 标签保留在元数据表中。未来若引入新模型(midjourney/flux/gemini),走同样的「场景体系归类 + 模型标签」方式,不再开模型来源顶层目录。
