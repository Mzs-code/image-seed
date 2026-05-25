# CLAUDE.md · Image Seed 项目工作指南

> 你的角色:作为这个**非代码、markdown 驱动**的图片库的协作 agent。主要工作是按既定规范帮用户归类新图、维护元数据、跑同步脚本。不写代码功能,除非脚本本身需要修。

个人 AI 生图参考/灵感库。非代码项目,Markdown 是主要展示方式。图片按「场景 × 风格/布局」两层结构组织,分类体系对齐 [baoyu-skills](https://github.com/JimLiu/baoyu-skills)。

## 术语速查

- **scenario(场景)**:顶层目录(`xhs-images/`、`infographic/` 等 12 个 + `unclassified/`)
- **substyle(子分类)**:场景下的二级分类(如 `infographic/grid-cards/`);扁平场景无 substyle
- **trunk**:图片 basename 去掉 `-NN` 重名后缀(`foo-01.jpg` → trunk `foo`),用于 sidecar 匹配
- **sidecar**:与图片成对的 `.md` 文件,存 prompt 内容(同 trunk 默认 / 跨 trunk `-template.md` 共享)
- **baoyu**:[baoyu-skills](https://github.com/JimLiu/baoyu-skills) 官方示例,统一后缀 `-baoyu.webp`,在画廊里永远排最后

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
- 扁平场景没有 substyle 段,直接 `<scenario-prefix>-<subject>.<ext>`,如 `poster-mortal-cultivation.webp`

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

## 图片归类

### Substyle 选择(infographic / xhs-images:styles vs layouts 冲突时)

`infographic`(17 styles + 20 layouts)和 `xhs-images`(9 styles + 6 layouts)的 substyle 分**画风(style)**和**布局(layout)**两类。一张图常同时匹配一个 style 和一个 layout(手绘讲义 + 9 宫格、sketch + 冰山等),但只能放一个目录。

**默认:画风优先,布局次之。** 同一作者/同 prompt 模板的一组图常画风一致但布局各异 — 按画风归类画廊里一眼识别成组,按布局归类会把同组拆散到 3–5 个 layout 目录,浏览价值低。布局信息保留在文件名 `<subject>-<modifier>` 段便于检索,如 `info-craft-handmade-autowired-iceberg.webp` 是 craft-handmade 画风的冰山图。

#### 强画风 vs 弱画风(决定是否迁)

**强画风 — 触发即按 style 归类**(画风有明确归属、识别度高,迁到对应 style 子分类):

| style | 视觉指纹 |
|---|---|
| `craft-handmade` | 浅色背景 + 手绘卡通边框 + pastel + 卡通角色/小怪兽(讲义风) |
| `cyberpunk-neon` | 深色背景 + 霓虹电光 + 赛博 UI / 黑客剪影 / 3D 机库 |
| `aged-academia` | 泛黄古卷 + 真人绘画 + 古典字体 |
| `bold-graphic` | 粗黑大数字 + 强色对比 + 极简版面 |
| `kawaii` | 萌系大眼睛卡通角色 + 萌系科普(**注意:仅 emoji + pastel 卡片不够强,不算**) |
| `chalkboard` `pixel-art` `claymation` `origami` `knolling` `lego-brick` `corporate-memphis` `storybook-watercolor` 等 | 各有强烈视觉指纹,触发即迁 |

**弱画风 — 保留 layout 子分类**(画风无对应 style 或元素弱):

- **蓝色单色手绘 sketch**(常见宝玉风):无对应 style,且 layout 信号往往很强 → 保留 layout
- **flat illustration**(扁平人物彩色插画):corporate-memphis 偏向抽象/几何企业风,具象人物归不进去 → 保留 layout
- **kawaii 元素弱**(几个 emoji + pastel + 圆角):不够强,保留 layout
- **3D isometric / minimal data viz / 卡通漫画**:infographic 内无对应 style → 保留 layout

#### 例外:布局优先的两种情况

1. 图就是该 layout 的「教科书示范」:纯结构图 / 空白模板 / 无明显画风(如线框黑白冰山图)
2. 图是 layout 类 baoyu 示例(`-baoyu.webp`),本就是 layout 词典的样板

#### 作者/系列识别(避免拆散同源图)

同一作者/同公众号/同 prompt 模板的图画风往往高度一致,**优先聚拢到同一 substyle**:

- **元数据「来源」字段** 是最强信号:`新智元` / `宝玉` / `GoWalker` / `NotebookLM` / `公众号·黑科技派` 等
- **图片签名/水印**(图角落公众号名)
- **标签里的模型/工具**:`gpt-image-2` / `baoyu-skills` 等
- **视觉一致性**:同样字体 / 同样色调 / 同样装饰元素(咖啡杯/星星/云朵/机器人吉祥物)

#### 「只有 baoyu」的 style 子分类是被忽视的目标

下载 baoyu 全集会预填很多"只有 1 张 baoyu"的 style 子分类(`aged-academia` / `bold-graphic` / `chalkboard` / `origami` / `pixel-art` 等)。归类时**主动检查这些 substyle** — 真实图视觉一旦匹配,激活该子分类比塞进 layout 更对。

#### 重复图检查(新增/迁移前必做)

1. **ls 目标目录**,检查文件名是否已存(基本同名 = 几乎确定重复)
2. 跨 substyle 时,**留意元数据描述高度相似的图**(同样标题、同样要点列表 = 高度怀疑)
3. 怀疑时用 Read 视觉对比,确认重复后保留**画风/语义更优**的版本,删除另一份

#### 踩过的坑

- **2026-05-25 早**:6 张 unclassified 投递的同系列手绘 sketch,初版按强 layout 信号(9 宫格 / 冰山)拆 2 张到 `grid-cards`/`iceberg`,与同组分离 → 全部回归 `craft-handmade`。
- **2026-05-25 晚 — 全量深扫**:扫 84 张非 baoyu infographic 图,发现 12 张拆错 + 1 张重复:
  - 5 张 cyberpunk-neon 系列(新智元)从 4 个 layout(timeline/journey/comparison/mind-map)收回
  - 4 张 craft-handmade 系列从 3 个 layout/style(grid-cards/mind-map/technical-schematic)收回
  - 1 张激活 `aged-academia`(从 technical-schematic 误归)
  - 1 张激活 `bold-graphic`(从 comparison-table 误归)
  - 1 张重复图(`craft-handmade/agent-architecture-cli` ≡ `circular-flow/agent-architecture` 视觉完全相同)删除
- 教训:layout 子分类是「画风不显著的容器」,一旦图自带强画风指纹就该迁出。「只有 baoyu 的 style」 + 「画风明显的 layout 候选图」是配对待激活的信号。

#### 系统化扫描方法(>50 张存量场景适用)

3 步漏斗,零成本筛 → 精准读图:

1. **Step 1 标签筛**:grep 各 layout 子分类元数据,找标签含画风词(`hand-drawn`/`pastel`/`kawaii`/`cyberpunk`/`craft-handmade`/`chalkboard`/`linework`/`cute-creature`/`handnote`/`sketch` 等)的图 — 这些是「自带画风标签却落在 layout」的直球嫌疑
2. **Step 2 同系列名称筛**:扫所有非 baoyu 图,找文件名共享 ≥4 字符 token(非通用词)且跨 ≥2 substyle 的图组 — 同 prompt/同主题被拆的信号
3. **Step 3 视觉验证**:对 Step 1+2 命中读图视觉对比;style 子分类的图作画风锚做对照

仅对 Step 1+2 命中读图,避免盲读全部存量。

### 并行 Read 错位(踩过的坑)

**并行 Read 多张图时,输出与调用顺序不一定 1:1 对应**,会导致内容与文件名错位、mv 后归类错乱。

- 优先**单图独读**判断内容,确认后再 mv
- 若并行读取,必须用文件大小/格式做交叉验证(如 jpeg 通常远小于 png),不能仅凭视觉印象按调用顺序对应
- mv 完成后,**至少抽读关键文件单独验证一次**(尤其新建子分类、文件名含强语义信息时)

## 标签约定

- 全小写、连字符、1–2 词:`warm` `rain` `cel-shading` `low-light` `pastel`
- 优先复用已有标签,避免 `dark`/`darkness`/`night-dark` 并存
- 仅在元数据表中用,反引号包裹(`` `rain` ``);便于 GitHub 仓库搜索跨场景命中
- **模型来源**也用标签记录:GPT Image 2 生成的图打 `` `gpt-image-2` `` 标签。未来增加 midjourney/flux/gemini 时同理(`` `midjourney` `` 等)

## 新增/修改图片后必须更新的地方

**single source of truth**:[CONTRIBUTING.md 「新增一张图」checklist](./CONTRIBUTING.md#新增一张图已明确分类)(12 步,含预处理 / sidecar / 元数据 / 脚本同步)。

本文件不再单独列步骤(避免与 CONTRIBUTING 内容 drift)。常见入口快捷方式:

- 投递新图 → CONTRIBUTING.md「投递到 unclassified」
- 归类暂存图 → CONTRIBUTING.md「从 unclassified 归类」
- 已直接分类 → CONTRIBUTING.md「新增一张图」

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

### `scripts/compress_images.py`

图片格式标准化 + 全仓 .md 引用同步替换。最常用:

```bash
# 投递 / 归类前预处理(规则:PNG 全转,JPG/JPEG > 10 MB 转)
scripts/compress_images.py unclassified/ --preset intake

# 全仓清扫
scripts/compress_images.py . --preset intake

# 通用阈值模式(老用法)
scripts/compress_images.py <path> --threshold-kb 1024
```

转换后自动 grep 替换 README / CLAUDE.md / CONTRIBUTING.md 等所有 .md 里的引用。配合 `gen_scenario_readmes.py` 让画廊数字同步。

### `scripts/mv-with-sidecar.sh`

归类时一次性搬图 + sidecar(同 basename / 同 trunk / 显式目标三种关联)。详见 CONTRIBUTING.md。

## 关键历史决策备忘

- **两层结构**:场景 → 子分类。不嵌 `styles/`/`layouts/` 子目录,扁平更直接。
- **子分类目录按需创建**:不预建空目录;有图才建,场景 README 的「可用子分类」清单作为"词典"引导。
- **无独立标签索引文件**:<200 张规模下,同步索引必然过期,改用「元数据反引号标签 + GitHub 搜索」。
- **图片格式规则**(2026-05 升级):**PNG 必转 WebP**(无损源,平均 -90%),**JPG/JPEG > 10 MB 转 WebP**(超大照片才动,避免普通 JPG 双重压缩);WebP / 小 JPG / 小 JPEG / GIF 保留原格式。工具:`scripts/compress_images.py --preset intake`。单图目标 < 500 KB。早期「不强制 webp」的旧规则已废除 —— 2026-05 一次性把仓库 50+ 张超标 PNG 转 WebP,共减重 124 MB / 72%。
- **2026-05 废弃 gpt-image-2 顶层目录**:原先曾用 `gpt-image-2/` 作为「按生成模型来源」的正交维度,实践发现与场景体系并行维护两套数字增加负担、且粒度对不齐。统一回归单一场景维度:7 个原 gpt-image-2 子分类(`poster`/`ecommerce`/`seasonal`/`travel`/`app-ui`/`anime`/`product-design`)升格为顶层扁平场景;`gpt-image-2/infographic` 17 张并入 `infographic/` 各 styles/layouts;`gpt-image-2/xhs` 3 张并入 `xhs-images/` 各 styles/layouts;模型来源以 `` `gpt-image-2` `` 标签保留在元数据表中。未来若引入新模型(midjourney/flux/gemini),走同样的「场景体系归类 + 模型标签」方式,不再开模型来源顶层目录。
