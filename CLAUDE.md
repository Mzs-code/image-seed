# CLAUDE.md · Image Seed 项目工作指南

个人 AI 生图参考/灵感库。非代码项目,Markdown 是主要展示方式。图片按「场景 × 风格/布局」两层结构组织,分类体系对齐 [baoyu-skills](https://github.com/JimLiu/baoyu-skills)。

## 目录结构

```
image-seed/
├── README.md                    # 总导航(场景表 + 按生成模型小节 + 精选墙)
├── CONTRIBUTING.md              # 新增/归类图片 checklist + 命名规范
├── CLAUDE.md                    # 本文件
├── .gitignore
├── <scenario>/                  # 场景目录
│   ├── README.md                # 场景画廊(3 列平铺,每图一格)
│   └── <substyle>/              # 子分类(有图才建)
│       ├── README.md            # 子分类画廊 + 元数据表
│       └── *.webp/jpg/png
├── gpt-image-2/                 # 按生成模型来源(补充维度,与场景正交)
│   ├── README.md                # 子分类导航 + 精选预览
│   └── <substyle>/              # 子分类(按内容类型,见下方表格)
│       ├── README.md            # 子分类画廊 + 元数据表
│       └── *.jpg/png
├── unclassified/                # 场景类图片待归类缓冲
├── unclassified-gpt-image-2/   # gpt-image-2 图片待归类缓冲
└── scripts/
    ├── gen_scenario_readmes.py  # 图片增删后必跑
    └── pull_baoyu.sh            # baoyu-skills 更新时重跑
```

## 场景与缩写

| 场景目录 | 文件名前缀 | 子分类维度 |
|---|---|---|
| `xhs-images/` | `xhs` | 9 styles + 6 layouts |
| `infographic/` | `info` | 17 styles + 20 layouts |
| `comic/` | `comic` | 6 layouts |
| `slide-deck/` | `deck` | 16 styles |
| `article-illustrator/` | `art` | 8 styles |
| `unclassified/` | `misc` | — |
| `gpt-image-2/` | `gpt-image-2` | ecommerce / infographic / xhs / seasonal / travel / app-ui / poster / anime / product-design |
| `unclassified-gpt-image-2/` | — | gpt-image-2 专属暂存区，处理完清空 |

子分类的完整名单见 `scripts/pull_baoyu.sh` 或各场景 README 的「可用子分类」小节。

## 文件命名规则

格式:`<scenario-prefix>-<substyle>-<subject>-<modifier>[-nn].<ext>`

- 仅 `a-z 0-9 -`,全小写连字符;总长 ≤ 70 字符
- 不用 `copy`/`new`/`final`/`v2` 等噪声词
- baoyu 官方示例统一后缀:`<prefix>-<substyle>-baoyu.webp`(下载脚本按此模式)
- 本地收藏图用语义化名:如 `deck-sketch-notes-how-ai-learns.jpg`

## 场景 README 布局规则(重要约束)

**3 列平铺大网格,每张图占一格。** 参考基准:baoyu-skills 的 README 风格,以及当前的 `infographic/README.md`。

核心规则:
1. **平铺结构**:一个大 3 列 Markdown 表格,所有子分类的所有图全在这一个表格里
2. **一张图一格**:子分类有 N 张图就占 N 个格子,同子分类的图**连续相邻排列**(相邻同标签 = 同组)
3. **本地图优先**:同一子分类下,非 baoyu 图排前,`-baoyu.webp` 排后
4. **缩略图尺寸**:不用 HTML `<img width>` 控制 — 依靠 markdown 3 列表格列宽自动均分,**前提是每行 3 格至少有 2 格有图**(否则空列坍缩导致残图被拉大)。当前实现因为平铺连续,天然满足
5. **不使用 H3 小节分段**:用户明确反馈分段式展开会让单张图占满列宽"太大",必须平铺
6. **点击行为**:缩略图和文字标签都跳转到 **子分类 README**(不跳图片,不跳目录)

运行 `python3 scripts/gen_scenario_readmes.py` 自动按以上规则重生成 5 个场景 README。

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

## gpt-image-2 子分类规则

gpt-image-2 目录与场景体系正交，按**内容类型**（而非 baoyu-skills 风格/布局）建子分类。

### 现有子分类

| 子分类 | 说明 |
|---|---|
| `ecommerce/` | 电商详情页、直播间 UI、搭配页 |
| `infographic/` | 知识百科、科普教育类信息图 |
| `xhs/` | 小红书风格图文：生活记录、穿搭指南 |
| `seasonal/` | 二十四节气、传统节日海报与手抄报 |
| `travel/` | 旅游目的地宣传海报 |
| `app-ui/` | 应用界面营销截图 |
| `poster/` | 影视/小说/品牌等单图宣传海报 |
| `anime/` | 动漫/漫画风格：分镜叙事、卡通人物、生活感故事图 |
| `product-design/` | 实物产品/工业设计/空间装置/创意设计概念图 |

### 命名与结构规则

- 文件名格式：`gpt-image-2-<substyle>-<subject>[-modifier].<ext>`，例如 `gpt-image-2-travel-guizhou-ink-map.jpeg`
- 子分类 README 格式与场景子分类相同：**画廊**（3 列平铺）+ **元数据表**
- `gpt-image-2/README.md` 维护为**子分类导航表 + 精选预览**格式（每个子分类各取 1 张代表图组成 3×2 网格）
- 新内容类型出现时，按需新建子分类目录（有图才建）

### unclassified-gpt-image-2 暂存区

- 专门存放待归类的 gpt-image-2 图片，处理完后清空
- 暂存文件可保留原始文件名（hash 名、序号名均可），归类时统一按上方命名规则改名
- 归类流程：确定内容类型 → 选择/新建子分类目录 → 移动并重命名 → 更新子分类 README → 更新 `gpt-image-2/README.md` 精选预览和导航表数字 → 更新根 README 图片数字

## 新增/修改图片后必须更新的地方

见 CONTRIBUTING.md 的 checklist,核心:

1. 子分类 README 的画廊和元数据表(手改)
2. 跑 `python3 scripts/gen_scenario_readmes.py`(自动更新 5 个场景 README 的平铺网格)
3. 根 README 的场景导航表数字(手改)

## 常用脚本

### `scripts/gen_scenario_readmes.py`

扫描各子分类目录下的实际图片文件,重新生成 5 个场景 README。**图片任何增删后都要跑**。核心逻辑:

- 按子分类顺序遍历,每张图一个 tile
- 本地图排前、baoyu 排后
- 输出 3 列 Markdown 表格,相邻同子分类标签=同组

### `scripts/pull_baoyu.sh`

从 baoyu-skills 仓库拉取全部 82 张示例图到本地对应子分类目录(带 `-baoyu.webp` 后缀)。仅在 baoyu-skills 更新、需要重新同步时运行。

**跑完必须对照去重清单手动删除已知重复项**(见脚本头注释)。

## 关键历史决策备忘

- **两层结构**:场景 → 子分类。不嵌 `styles/`/`layouts/` 子目录,扁平更直接。
- **子分类目录按需创建**:不预建空目录;有图才建,场景 README 的「可用子分类」清单作为"词典"引导。
- **无独立标签索引文件**:<200 张规模下,同步索引必然过期,改用「元数据反引号标签 + GitHub 搜索」。
- **不强制 webp**:GitHub 对 jpg/png 渲染更稳,单图 < 1MB 即可,格式混用无妨。
- **gpt-image-2 作顶层目录**:与场景正交的「按生成模型来源」分类维度,放在根 README 独立小节。未来增加 midjourney/flux/gemini 时沿用此模式。
- **gpt-image-2 内部按内容类型分子分类**:图片量增长后发现「纯按模型来源平铺」不够用，改为 ecommerce/infographic/xhs/seasonal/travel/app-ui/poster 七类。子分类策略与场景体系无关，按实际内容决定；新类型出现时按需新增。
- **unclassified-gpt-image-2 作独立暂存区**:与 `unclassified/`（场景类）分开，避免混用。
