# 如何新增 / 归类图片

## 新增一张图(已明确分类)

1. [ ] 选场景 + 子分类(拿不准 → `unclassified/`)
2. [ ] 压缩到 <1MB(`jpg` q=85 / `webp` q=80)
3. [ ] 重命名:`<scenario>-<substyle>-<subject>-<modifier>[-nn].<ext>`,全小写连字符
4. [ ] 若该子分类目录不存在 → 新建目录(如 `xhs-images/cute/`)
5. [ ] 拷贝图片到子分类目录
6. [ ] 若是该子分类第一张图:
   - 在子分类目录新建 `README.md`(按[子分类模板](#子分类-readme-模板))
   - 选一张作为封面(命名 `<scenario>-<substyle>-cover.jpg`,或在场景 README 里直接引用某张现有图)
   - 在场景 README 的对应画廊里追加该子分类的卡片(解除该行的空单元格占位)
7. [ ] 在子分类 README「画廊」表追加一格,保持 3 列(不足补空单元格)
8. [ ] 在子分类 README「元数据」表追加一行,来源/prompt 缺失填 `—`
9. [ ] (可选)若代表性极强,替换根 README「精选墙」里该场景的旧图
10. [ ] 更新根 README「场景导航」表的「现有图片」数量
11. [ ] Commit:`add(<scenario>/<substyle>): <subject>-<modifier>`

## 从 unclassified 归类

1. [ ] 确定场景 + 子分类
2. [ ] `git mv unclassified/xxx.jpg <scenario>/<substyle>/<scenario-short>-<substyle>-xxx.jpg`
3. [ ] 若目标子分类首次建立,按上方第 6 步建 README + 接入场景画廊
4. [ ] 子分类 README 追加画廊 + 元数据行
5. [ ] `unclassified/README.md` 画廊里删除对应单元格
6. [ ] Commit:`move: xxx → <scenario>/<substyle>`

## 命名规范

**格式**:`<scenario>-<substyle>-<subject>-<modifier>[-nn].<ext>`

| 部分 | 规则 | 示例 |
|---|---|---|
| scenario | 场景缩写,全小写 | `xhs` `info` `comic` `deck` `art` `misc` |
| substyle | 子分类名,全小写(同目录名) | `cute` `cyberpunk-neon` `pixel-art` `mind-map` |
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

## 场景缩写表

| 场景目录 | 缩写 |
|---|---|
| `xhs-images/` | `xhs` |
| `infographic/` | `info` |
| `comic/` | `comic` |
| `slide-deck/` | `deck` |
| `article-illustrator/` | `art` |
| `unclassified/` | `misc` |

**按生成模型来源**(补充维度,目录名即前缀):

| 顶层目录 | 文件名前缀 |
|---|---|
| `gpt-image-2/` | `gpt-image-2` |

## 标签约定

- 全小写、连字符、1–2 词:`warm` `rain` `cel-shading` `low-light` `pastel`
- 优先复用已有标签,避免 `dark` / `darkness` / `night-dark` 并存
- 在元数据表用反引号包裹:`` `rain` `` — 便于 GitHub 仓库搜索跨场景命中

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
