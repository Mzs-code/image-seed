# 如何新增 / 归类图片

## 新增一张图(已明确分类)

1. [ ] 选场景 + 子分类(拿不准 → `unclassified/`)
2. [ ] 压缩到 <1MB(`jpg` q=85 / `webp` q=80)
3. [ ] 重命名:`<scenario-prefix>-[<substyle>-]<subject>-<modifier>[-nn].<ext>`,全小写连字符。扁平场景(`poster/`、`ecommerce/` 等)无 substyle 段
4. [ ] 若该子分类目录不存在 → 新建目录(如 `xhs-images/cute/`)
5. [ ] 拷贝图片到目标目录
6. [ ] 若是该子分类第一张图:
   - 在子分类目录新建 `README.md`(按[子分类模板](#子分类-readme-模板))
   - 在场景 README 的对应画廊里追加该子分类的卡片(解除该行的空单元格占位)
7. [ ] 在子分类 README(或扁平场景 README)的「画廊」表追加一格,保持 3 列(不足补空单元格)
8. [ ] 在「元数据」表追加一行,来源/prompt 缺失填 `—`。若由 GPT Image 2 生成,标签加 `` `gpt-image-2` ``
9. [ ] (可选)若代表性极强,替换根 README「精选墙」里该场景的旧图
10. [ ] 跑 `python3 scripts/gen_scenario_readmes.py`(仅 5 个非扁平场景受影响)
11. [ ] 更新根 README「场景导航」表的「现有图片」数量
12. [ ] Commit:`add(<scenario>/<substyle>): <subject>-<modifier>`

## 从 unclassified 归类

1. [ ] 确定场景 + 子分类
2. [ ] `git mv unclassified/xxx.jpg <scenario>/<substyle>/<scenario-prefix>-<substyle>-xxx.jpg`(扁平场景去掉 `<substyle>` 段)
3. [ ] 若目标子分类首次建立,按上方第 6 步建 README + 接入场景画廊
4. [ ] 子分类 README(或扁平场景 README)追加画廊 + 元数据行
5. [ ] `unclassified/README.md` 画廊里删除对应单元格
6. [ ] Commit:`move: xxx → <scenario>/<substyle>`

## 命名规范

**格式**:`<scenario-prefix>-[<substyle>-]<subject>-<modifier>[-nn].<ext>`

| 部分 | 规则 | 示例 |
|---|---|---|
| scenario-prefix | 场景缩写,全小写 | `xhs` `info` `comic` `deck` `art` `poster` `appui` `prod` `misc` |
| substyle | 子分类名,全小写(同目录名)。扁平场景无此段 | `cute` `cyberpunk-neon` `pixel-art` `mind-map` |
| subject | 主体,1–2 词 | `girl` `city` `process` |
| modifier | 场景/修饰,1–3 词 | `cafe` `night-neon` `cover` |
| nn | 重名编号,两位数 | `-01` `-02` |
| ext | 小写扩展名 | `.jpg` `.png` `.webp` |

**字符规则**:仅 `a-z 0-9 -`;不用下划线/空格/中文/大写;总长 ≤ 70 字符;禁用 `copy`/`new`/`final`/`v2` 等噪声。

**示例**:

- `xhs-cute-girl-cafe.jpg`
- `info-cyberpunk-neon-ai-process.jpg`
- `deck-blueprint-cover.jpg`
- `comic-webtoon-fight-scene-01.png`
- `art-watercolor-mountain-dawn.webp`
- `poster-mortal-cultivation.png`(扁平,无 substyle)
- `seasonal-lixia-handnote.png`(扁平)

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

## 子分类 README 模板

```markdown
# <Scenario> · <Substyle>

<一句话描述该风格/布局的视觉特征>

[← 返回场景索引](../README.md) | [← 返回总索引](../../README.md)

## 画廊

|   |   |   |
|:---:|:---:|:---:|
| [![<filename>](./<filename>.jpg)](./<filename>.jpg) | ... | ... |
| <short-label> | ... | ... |

## 元数据

| 文件 | 主体 | 标签 | 来源 | Prompt |
|---|---|---|---|---|
| [<filename>](./<filename>.jpg) | ... | `tag1` `tag2` | [source](https://...) 或 — | `prompt 文本` 或 — |

**说明**:来源/Prompt 缺失填 `—`;标签用反引号包裹。
```

扁平场景(`poster/`、`ecommerce/` 等)的 `README.md` 结构相同,但返回链接只有一级:`[← 返回总索引](../README.md)`。
