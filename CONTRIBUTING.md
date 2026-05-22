# 如何新增 / 归类图片

## 新增一张图(已明确分类)

1. [ ] 选场景 + 子分类(拿不准 → `unclassified/`)
2. [ ] **预处理图片**(规范化格式):跑 `scripts/compress_images.py <图所在目录> --preset intake`,自动:
   - 所有 PNG → WebP(无损源,zero-risk;90%+ 减重)
   - 所有 JPG/JPEG **> 10 MB** → WebP(超大照片才动,避免普通 JPG 双重压缩)
   - 同步替换全仓 .md 里的引用
   - 跑完得到 `.webp` 替代品
3. [ ] 重命名:`<scenario-prefix>-[<substyle>-]<subject>-<modifier>[-nn].<ext>`,全小写连字符。扁平场景(`poster/`、`ecommerce/` 等)无 substyle 段
4. [ ] 若该子分类目录不存在 → 新建目录(如 `xhs-images/cute/`)
5. [ ] 拷贝图片到目标目录
6. [ ] 若是该子分类第一张图:
   - 在子分类目录新建 `README.md`(按[子分类模板](#子分类-readme-模板))
   - 在场景 README 的对应画廊里追加该子分类的卡片(解除该行的空单元格占位)
7. [ ] **画廊段不手编**:跳过(由脚本自动生成,见步骤 10)
8. [ ] 若有 prompt → 同时新建 [sidecar 文件](#prompt-sidecar-文件)`<trunk>.md`,与图片同目录(trunk = basename 去掉 `-NN` 重名后缀;多图共享 prompt 时 N 张图指向同一个 sidecar,详见 [多图共享 prompt](#多图共享-prompt))
9. [ ] 在子分类 README(或扁平场景 README)的「元数据」表追加一行,来源缺失填 `—`;Prompt 列:有 sidecar 写 `[prompt: <20 字内摘要>…](./<trunk>.md)`(摘要让链接在表格里也能识别),无则填 `—`。若由 GPT Image 2 生成,标签加 `` `gpt-image-2` ``
10. [ ] 跑 `python3 scripts/gen_scenario_readmes.py` —— 该脚本一站式完成:重生成 5 个非扁平场景 README + 重写所有子分类 / 扁平场景 README 的画廊段(`## 画廊` 到下一个 `## ` 之间)+ 给带 sidecar 的图加 📝 角标 + 回填根 README 场景导航图片数
11. [ ] (可选)若代表性极强,替换根 README「精选墙」里该场景的旧图
12. [ ] Commit:`add(<scenario>/<substyle>): <subject>-<modifier>`

## 从 unclassified 归类

1. [ ] 确定场景 + 子分类
2. [ ] **推荐用 `scripts/mv-with-sidecar.sh <旧路径无扩展名> <新路径无扩展名>`** —— 自动一次性搬图 + 同 trunk sidecar(若存在),不漏 / 不脱钩。如:
   ```bash
   scripts/mv-with-sidecar.sh unclassified/1 infographic/craft-handmade/info-craft-handmade-fourier-transform
   ```
   不用脚本时,普通 `mv` 即可(暂存文件多半未 `git add`,`git mv` 会失败);**搬图后务必检查同 trunk 的 `.md` 也搬走了**
3. [ ] 若目标子分类首次建立,按上方第 6 步建 README + 接入场景画廊
4. [ ] 子分类 README(或扁平场景 README)只追加**元数据**行(Prompt 列按 sidecar 有无填 `[prompt: <摘要>…](./<trunk>.md)` 或 `—`);画廊段不动 —— 脚本会自动重写
5. [ ] 跑 `python3 scripts/gen_scenario_readmes.py`(自动重生成场景 README + 子分类画廊段 + 根 README 数字)
6. [ ] Commit:`move: xxx → <scenario>/<substyle>`

## 投递到 unclassified(暂存)

拿不准场景时,先丢到 `unclassified/`,后续再用「从 unclassified 归类」流程处理。

1. [ ] 图片直接放入 `unclassified/`,文件名可保留原始名(如 `screenshot-2026-05-21.jpg`、`IMG_8421.png`)
2. [ ] **若有 prompt → 同时新建同 basename 的 sidecar**:`unclassified/screenshot-2026-05-21.md`(和图片成对放,后续 `git mv` 一起搬)
3. [ ] **(推荐)预处理图片格式**:
   ```bash
   scripts/compress_images.py unclassified/ --preset intake
   ```
   投递时图通常未被任何 .md 引用,跑完只改文件本身,零外部影响。归类前文件已是 `.webp`(或本来就是合规格式),`mv-with-sidecar.sh` 自动识别扩展名跟着搬。
4. [ ] 不必更新 `unclassified/README.md` 画廊(归类时再处理)

> 设计动机:sidecar 与图片同 basename 是「图文成对」的唯一可靠机制 —— 暂存时建立的配对,归类时一并 `git mv`,不会因为忘了搬 prompt 而脱钩。

## 图片格式规则

| 输入格式 | 处理 | 原因 |
|---|---|---|
| PNG | **必转 WebP** | 无损源,转 WebP 平均 -90%,几乎零质量损失;不会双重压缩 |
| JPG/JPEG ≤ 10 MB | 保留 | 已 lossy,再 WebP 有双重压缩风险;体积可控 |
| JPG/JPEG > 10 MB | **必转 WebP** | 超大照片体量收益压过质量损失 |
| WebP | 保留 | 已是目标格式 |
| GIF | 保留 | 动图,不动 |

实施工具:`scripts/compress_images.py --preset intake` 自动按这套规则处理。预设详情见脚本头注释。

**单图大小目标**:< 500 KB(WebP 经 intake 处理后,信息图 / 海报 / 插画都能达到)。GitHub 单文件上限 100 MB,LFS 上限更高,但我们的目标是渲染流畅 / 国内访问 / 仓库克隆轻。

## 命名规范

**格式**:`<scenario-prefix>-[<substyle>-]<subject>-<modifier>[-nn].<ext>`

| 部分 | 规则 | 示例 |
|---|---|---|
| scenario-prefix | 场景缩写,全小写 | `xhs` `info` `comic` `deck` `art` `poster` `appui` `prod` `misc` |
| substyle | 子分类名,全小写(同目录名)。扁平场景无此段 | `cute` `cyberpunk-neon` `pixel-art` `mind-map` |
| subject | 主体,1–2 词 | `girl` `city` `process` |
| modifier | 场景/修饰,1–3 词 | `cafe` `night-neon` `cover` |
| nn | 重名/变体编号,**推荐两位数从 `-01` 起便于排序**;实际接受 `-0`/`-N`/`-NN`/`-NNN` 任意位数 | `-01` `-02` `-1` `-2` `-0` |
| ext | 小写扩展名(图片);prompt sidecar 用 `.md` | `.jpg` `.png` `.webp` / `.md` |

**字符规则**:仅 `a-z 0-9 -`;不用下划线/空格/中文/大写;总长 ≤ 70 字符;禁用 `copy`/`new`/`final`/`v2` 等噪声。

**示例**:

- `xhs-cute-girl-cafe.jpg`
- `info-cyberpunk-neon-ai-process.jpg`
- `deck-blueprint-cover.jpg`
- `comic-webtoon-fight-scene-01.png`
- `art-watercolor-mountain-dawn.webp`
- `poster-mortal-cultivation.webp`(扁平,无 substyle)
- `seasonal-lixia-handnote.webp`(扁平)

## 场景缩写表

| 场景目录 | 缩写 | 结构 |
|---|---|---|
| `xhs-images/` | `xhs` | styles + layouts |
| `infographic/` | `info` | styles + layouts |
| `comic/` | `comic` | layouts |
| `slide-deck/` | `deck` | styles |
| `article-illustrator/` | `art` | styles |
| `poster/` | `poster` | 扁平 |
| `ecommerce/` | `ecommerce` | 扁平 |
| `seasonal/` | `seasonal` | 扁平 |
| `travel/` | `travel` | 扁平 |
| `app-ui/` | `appui` | 扁平 |
| `anime/` | `anime` | 扁平 |
| `product-design/` | `prod` | 扁平 |
| `unclassified/` | `misc` | 暂存 |

## 标签约定

- 全小写、连字符、1–2 词:`warm` `rain` `cel-shading` `low-light` `pastel`
- 优先复用已有标签,避免 `dark` / `darkness` / `night-dark` 并存
- 在元数据表用反引号包裹:`` `rain` `` — 便于 GitHub 仓库搜索跨场景命中
- **模型来源**也用标签记录:GPT Image 2 生成的图打 `` `gpt-image-2` `` 标签

## Prompt sidecar 文件

部分图片有原始 prompt。**Prompt 不进 README 表格内联**(多段/特殊字符会破坏 Markdown 渲染),改为 `.md` 文件作为 sidecar 与图片成对存放。

### 核心规则

1. **同 trunk(默认)**:sidecar 名是图片 basename 去掉 `-NN` 重名后缀得到的 trunk
   - 单图:`poster-foo.png` ↔ `poster-foo.md`(无 `-NN`,trunk = basename)
   - 多图共享 prompt:`poster-foo-01.png` / `-02.png` / `-03.png` ↔ 同一份 `poster-foo.md`
   - 查找规则统一:image `X-NN.ext` → sidecar `X.md`;image `X.ext` → sidecar `X.md`
2. **同目录**:sidecar 与图片放在一起,不另开 `prompts/` 子目录
3. **无 prompt 不建文件**:没有就是没有,README 元数据表 Prompt 列填 `—`
4. **`unclassified/` 同样适用**:暂存阶段就维持图文成对,归类时一起 `mv`

### 文件格式(松约束)

sidecar **不强制任何结构**,目标是「以人为本、易写易读」。最简形式就是一段中文/英文 prompt 文本。

可选增强:

- **顶部加图片预览**(强烈推荐,让 sidecar 自包含):
  ```markdown
  ![preview](./info-craft-handmade-fourier-transform.jpg)

  ## 傅里叶变换数学可视化

  <prompt 正文>
  ```
- **frontmatter 全选填**,有就写、没有就省。常见字段:
  ```yaml
  ---
  model: gpt-image-2            # 与 README 标签 `gpt-image-2` 对齐
  source: https://...           # 原图/原 prompt 来源(选填)
  params:                       # 模型参数(选填,只填知道的)
    aspect_ratio: 3:4
    seed: 12345
  variants:                     # 多变体差异(选填,见下文)
    - { file: foo-01.png, seed: 12345 }
    - { file: foo-02.png, seed: 67890, note: 颜色更暖 }
  ---
  ```
- **prompt 正文随意 markdown**:可用段落、blockquote、加粗、列表自由组织。**不强制 `​```text` 围栏** —— 只在 prompt 含大量特殊字符(`{}<>` 等)需原样保留时再用
- **结尾可选 `## Notes`** 写迭代笔记、负面 prompt 等

### 多图共享 prompt

一个 prompt 通过种子/参数微调或重抽生成多张图,**不要复制 sidecar**,共用一份。

- 图片用数字后缀区分变体:`poster-foo-01.png` / `-02.png` / `-03.png`(推荐两位数从 `-01` 起;`-0`/`-1`/`-N` 也接受,只要同组保持一致)
- sidecar 取共同 trunk:`poster-foo.md`(一份)
- README 元数据表 N 行图都链接到同一个 sidecar,语义自然(多行指向同一处 = 变体组)
- per-variant 差异(seed/aspect/微调点)写在 sidecar frontmatter 的 `variants:` 列表(见上文示例),或正文 `## Notes` 段

**Trunk 唯一性**(建议而非强制):同一目录内尽量给独立单图与变体组用不同 trunk,避免撞车。撞车时给变体组加更具体的修饰(`poster-foo-cat-01.png`)。

### Prompt 模板(同一份 prompt 应用于不同主题图)

特殊情形:你有一段 prompt 模板含占位符(如 `【数学概念/知识点】`、`{请输入你的内容或者参考图片}`),用它生成主题各异的多张图(傅里叶、贝叶斯、拉普拉斯…或 Claude Managed Agents / Hermes Agent / C4 Banking…)。

这些图**主题不同**(不是变体),但**模板共享**。两种处理任选:

- **(简)各图各自 sidecar,内容复制模板**:`info-craft-handmade-fourier-transform.md` / `-bayes.md` / `-laplace.md` 各一份。drift 风险但路径最直观
- **(优)共用一份模板 sidecar,各图 README 都链接它**(推荐):sidecar 文件名后缀加 `-template.md`,如 `info-craft-handmade-knowledge-diagram-template.md`。各图 README 元数据 Prompt 列都写 `[prompt: <模板摘要>…](./info-craft-handmade-knowledge-diagram-template.md)`,链接共指。此时 trunk 同名约定**放宽**:sidecar 名不必等于图 trunk

**实际操作(option 2)**:
1. 6 张图各自语义命名(如 `info-craft-handmade-claude-managed-agents.jpeg` / `-hermes-agent.jpeg` …)
2. sidecar 单独命名:`info-craft-handmade-knowledge-diagram-template.md`
3. 用 `mv-with-sidecar.sh` 的第三参数显式指定 sidecar 目标:
   ```bash
   scripts/mv-with-sidecar.sh unclassified/1-0 \
     infographic/craft-handmade/info-craft-handmade-claude-managed-agents \
     infographic/craft-handmade/info-craft-handmade-knowledge-diagram-template
   ```
   后续 5 张图重复跑同命令(改 src 和 dst-img),sidecar 已在目标位置时自动跳过
4. README 元数据各行加 `` `template-shared` `` 标签便于识别;Prompt 列都指向同一份 sidecar
5. **角标识别**:`gen_scenario_readmes.py` 通过扫元数据 Prompt 列(而非文件名)决定角标 —— 所以**只要元数据填了链接,就会正确加 📝**,无论是同 trunk 还是模板共享

### README 元数据表的 Prompt 列

| 情况 | Prompt 列写法 |
|---|---|
| 有 sidecar | `[prompt: <20 字内摘要>…](./<trunk>.md)` —— **链接文本带摘要**,让表格里直接能识别 |
| 无 prompt | `—` |
| ~~内联反引号 prompt 文本~~ | **已废弃**,新增/编辑时顺手转 sidecar |

**为什么链接带摘要**:表格里 N 行 prompt 都写「prompt」纯链接时,行间无差异、识别价值低。带 20 字摘要让浏览者扫一眼就知道每行 prompt 大概讲什么。摘要不必工整,关键词即可。

示例:
- `[prompt: 数学可视化讲义风模板…](./info-craft-handmade-fourier-transform.md)`
- `[prompt: 赛博朋克霓虹城市夜景…](./poster-cyber-night.md)`

### 与 `gen_scenario_readmes.py` 的关系

脚本(自动)做四件事,你不用手动维护:

1. 重生成 5 个非扁平场景的平铺网格 README
2. **重写所有子分类 + 7 个扁平场景 README 的「画廊」段**(以 `## 画廊` 为锚,到下一个 `## ` 标题之前的内容会被完全替换;只动画廊,元数据段不动)
3. **扫子分类元数据表 Prompt 列,在场景网格的 label 行加 📝 角标**(元数据驱动 — 只要 Prompt 列有 `[prompt: …](./….md)` 链接,该图就会被识别;同 trunk / 同 basename / 跨 trunk 模板共享三种情形统一处理)
4. **回填根 README 场景导航表的「现有图片」数字**(扫各场景图片数,不数 sidecar)

跑法不变:`python3 scripts/gen_scenario_readmes.py`。

**注意事项**:
- 画廊段由脚本控制 —— 不要在画廊里写注释或自定义排序,会被下次跑脚本覆盖
- 排序规则:本地图 alphabetical + `*-baoyu.webp` 永远最后
- 如果元数据表少了某些图(而画廊里有),脚本不会告警 —— 但画廊会自动包含所有图片文件,所以"画廊有 N 张图、元数据只有 M 行"的不一致一眼可见(可以拿这做查漏)

### 搬迁助手 `scripts/mv-with-sidecar.sh`

归类时一次性搬图 + 同 trunk sidecar(若存在):

```bash
scripts/mv-with-sidecar.sh <src-no-ext> <dst-no-ext>
# 例:
scripts/mv-with-sidecar.sh unclassified/1 infographic/craft-handmade/info-craft-handmade-fourier-transform
```

自动识别图片扩展名(`.jpg`/`.png`/`.jpeg`/`.webp`/`.gif`),并搬同名 `.md`(若存在)。变体组只需对每张图各跑一次,sidecar 会在第一次搬完后自动跳过。

## 子分类 README 模板

```markdown
# <Scenario> · <Substyle>

<一句话描述该风格/布局的视觉特征>

[← 返回场景索引](../README.md) | [← 返回总索引](../../README.md)

## 画廊

<!-- 由 scripts/gen_scenario_readmes.py 自动生成,勿手编 -->
|   |   |   |
|:---:|:---:|:---:|
| [![<filename>](./<filename>.jpg)](./<filename>.jpg) | ... | ... |
| <short-label> | ... | ... |

## 元数据

| 文件 | 主体 | 标签 | 来源 | Prompt |
|---|---|---|---|---|
| [<filename>](./<filename>.jpg) | ... | `tag1` `tag2` | [source](https://...) 或 — | [prompt: <摘要>…](./<trunk>.md) 或 — |

**说明**:来源缺失填 `—`;Prompt 有 sidecar 写带 20 字摘要的链接 `[prompt: <摘要>…](./<trunk>.md)`(trunk = basename 去 `-NN`,多图共享时多行指向同一个 sidecar),无则填 `—`;标签用反引号包裹。
```

扁平场景(`poster/`、`ecommerce/` 等)的 `README.md` 结构相同,但返回链接只有一级:`[← 返回总索引](../README.md)`。
