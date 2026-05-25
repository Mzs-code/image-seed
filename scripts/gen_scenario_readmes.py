#!/usr/bin/env python3
"""生成场景 README + 同步根 README 图片数 + sidecar 角标。

跑这一个脚本完成:
1. 重生成 5 个非扁平场景 README(3 列大网格平铺,每图一格)
2. 给带同 trunk `.md` sidecar 的图,在 label 行加 📝 角标
3. 扫描所有场景图片数,回填根 README「场景导航」表「现有图片」列
"""
import os
import re

ROOT = "/Users/maozhenshou/Documents/AICode/image-seed"

# 扁平场景:目录名 → 文件名前缀(无 substyle 段)
FLAT_PREFIXES = {
    "poster": "poster",
    "ecommerce": "ecommerce",
    "seasonal": "seasonal",
    "travel": "travel",
    "app-ui": "appui",
    "product-design": "prod",
}
FLAT_SCENARIOS = list(FLAT_PREFIXES.keys())
UNCLASSIFIED = "unclassified"

SCENARIOS = {
    "xhs-images": {
        "title": "XHS Images",
        "zh": "小红书图片",
        "prefix": "xhs",
        "desc": "社交平台配图,封面/笔记头图。分 **Styles(视觉风格)** 与 **Layouts(排版布局)** 两个维度。",
        "styles": ["cute", "fresh", "warm", "bold", "minimal", "retro", "pop", "notion", "chalkboard"],
        "layouts": ["sparse", "balanced", "dense", "list", "comparison", "flow"],
    },
    "infographic": {
        "title": "Infographic",
        "zh": "信息图",
        "prefix": "info",
        "desc": "信息可视化、概念图解、知识卡片。分 **Styles(视觉风格)** 与 **Layouts(布局结构)** 两个维度。",
        "styles": ["craft-handmade", "claymation", "kawaii", "storybook-watercolor", "chalkboard", "cyberpunk-neon", "bold-graphic", "aged-academia", "corporate-memphis", "technical-schematic", "origami", "pixel-art", "ui-wireframe", "subway-map", "ikea-manual", "knolling", "lego-brick"],
        "layouts": ["bridge", "circular-flow", "comparison-table", "do-dont", "equation", "feature-list", "fishbone", "funnel", "grid-cards", "iceberg", "journey-path", "layers-stack", "mind-map", "nested-circles", "priority-quadrants", "pyramid", "scale-balance", "timeline-horizontal", "tree-hierarchy", "venn"],
    },
    "comic": {
        "title": "Comic",
        "zh": "漫画",
        "prefix": "comic",
        "desc": "漫画分镜、连环画、长条漫(webtoon)等。仅有 **Layouts(布局)** 维度。",
        "styles": [],
        "layouts": ["standard", "cinematic", "dense", "splash", "mixed", "webtoon"],
    },
    "slide-deck": {
        "title": "Slide Deck",
        "zh": "演示文稿",
        "prefix": "deck",
        "desc": "幻灯片、Keynote、Pitch Deck 等演示场景。仅有 **Styles(视觉风格)** 维度。",
        "styles": ["blueprint", "chalkboard", "bold-editorial", "corporate", "dark-atmospheric", "editorial-infographic", "fantasy-animation", "intuition-machine", "minimal", "notion", "pixel-art", "scientific", "sketch-notes", "vector-illustration", "vintage", "watercolor"],
        "layouts": [],
    },
    "article-illustrator": {
        "title": "Article Illustrator",
        "zh": "文章插图",
        "prefix": "art",
        "desc": "博客、公众号、知识文章的配图。仅有 **Styles(视觉风格)** 维度。",
        "styles": ["notion", "elegant", "warm", "minimal", "blueprint", "watercolor", "editorial", "scientific"],
        "layouts": [],
    },
}


IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif")
NN_SUFFIX_RE = re.compile(r"-\d+$")  # 接受 -N / -NN / -NNN,放宽以容纳自然写法


def list_images_in(d):
    """目录里仅图片文件(排除 .md sidecar、README、其他)。"""
    if not os.path.isdir(d):
        return []
    return [f for f in os.listdir(d)
            if f.lower().endswith(IMAGE_EXTS)
            and os.path.isfile(os.path.join(d, f))]


def collect_images(scenario, substyle):
    """该子分类下所有图,本地图优先,baoyu 排最后。"""
    d = os.path.join(ROOT, scenario, substyle)
    files = list_images_in(d)
    non_baoyu = sorted(f for f in files if not f.endswith("-baoyu.webp"))
    baoyu = sorted(f for f in files if f.endswith("-baoyu.webp"))
    return non_baoyu + baoyu


_PROMPT_CACHE = {}
_PROMPT_MAP_CACHE = {}
_META_CACHE = {}
META_HEAD_RE = re.compile(r"^## 元数据\s*$", re.MULTILINE)
META_ROW_RE = re.compile(r"^\| \[([^\]]+)\]")
PROMPT_LINK_RE = re.compile(r"\[prompt[^\]]*\]\([^)]+\.md\)")
PROMPT_LINK_PATH_RE = re.compile(r"\[prompt[^\]]*\]\(([^)]+\.md)\)")
TAG_RE = re.compile(r"`([^`]+)`")


def _esc(s):
    """最小 HTML 转义:画廊嵌入的主体/标签可能含 < > & " 等字符。"""
    if not s:
        return ""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def _read_meta_table(scenario, substyle):
    """读元数据表,返回 {stem: (subject, [tags])}。substyle=None 用于扁平场景。

    元数据表每行格式(管道分隔):
        | [stem](./stem.ext) | 主体描述 | `tag1` `tag2` ... | 来源 | Prompt |
    主体缺失时表里写「—」,转成空串。
    """
    key = (scenario, substyle)
    if key in _META_CACHE:
        return _META_CACHE[key]
    d = os.path.join(ROOT, scenario, substyle) if substyle else os.path.join(ROOT, scenario)
    readme = os.path.join(d, "README.md")
    out = {}
    if not os.path.isfile(readme):
        _META_CACHE[key] = out
        return out
    with open(readme) as f:
        text = f.read()
    head = META_HEAD_RE.search(text)
    if not head:
        _META_CACHE[key] = out
        return out
    body = text[head.end():]
    nxt = re.search(r"^## ", body, re.MULTILINE)
    if nxt:
        body = body[:nxt.start()]
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("| ["):
            continue
        parts = [p.strip() for p in line.split("|")]
        # 期望:['', '[stem](./..)', subject, tags, source, prompt, '']
        if len(parts) < 5:
            continue
        m = re.match(r"^\[([^\]]+)\]", parts[1])
        if not m:
            continue
        stem = m.group(1)
        subject_raw = parts[2]
        subject = "" if subject_raw in ("—", "-", "") else subject_raw
        tags = TAG_RE.findall(parts[3])
        out[stem] = (subject, tags)
    _META_CACHE[key] = out
    return out


def _get_prompt_set(scenario, substyle):
    """扫子分类(或扁平场景)README 元数据段,返回带 prompt 链接的图 stem 集合。

    元数据驱动 angle 优于文件命名约定:
    - 单图同 basename / 多变体同 trunk / 跨 trunk 共享模板,三种情形统一识别
    - 与用户实际看到的 README 表格一致(no false positive)
    """
    key = (scenario, substyle)
    if key in _PROMPT_CACHE:
        return _PROMPT_CACHE[key]
    d = os.path.join(ROOT, scenario, substyle) if substyle else os.path.join(ROOT, scenario)
    readme = os.path.join(d, "README.md")
    stems = set()
    if os.path.isfile(readme):
        with open(readme) as f:
            text = f.read()
        head = META_HEAD_RE.search(text)
        if head:
            body = text[head.end():]
            # 截到下一个 H2 之前
            nxt = re.search(r"^## ", body, re.MULTILINE)
            if nxt:
                body = body[:nxt.start()]
            for line in body.splitlines():
                row = META_ROW_RE.match(line)
                if row and PROMPT_LINK_RE.search(line):
                    stems.add(row.group(1))
    _PROMPT_CACHE[key] = stems
    return stems


def has_sidecar(scenario, substyle, image_filename):
    """该图是否有 prompt:以元数据表 Prompt 列为准(非文件系统检查)。"""
    stem = image_filename.rsplit(".", 1)[0]
    return stem in _get_prompt_set(scenario, substyle)


def _get_prompt_map(scenario, substyle):
    """{stem: sidecar_md_path},直接从元数据表 Prompt 列的 markdown 链接抓取。"""
    key = (scenario, substyle)
    if key in _PROMPT_MAP_CACHE:
        return _PROMPT_MAP_CACHE[key]
    d = os.path.join(ROOT, scenario, substyle) if substyle else os.path.join(ROOT, scenario)
    readme = os.path.join(d, "README.md")
    out = {}
    if not os.path.isfile(readme):
        _PROMPT_MAP_CACHE[key] = out
        return out
    with open(readme) as f:
        text = f.read()
    head = META_HEAD_RE.search(text)
    if not head:
        _PROMPT_MAP_CACHE[key] = out
        return out
    body = text[head.end():]
    nxt = re.search(r"^## ", body, re.MULTILINE)
    if nxt:
        body = body[:nxt.start()]
    for line in body.splitlines():
        row = META_ROW_RE.match(line)
        if not row:
            continue
        m = PROMPT_LINK_PATH_RE.search(line)
        if m:
            out[row.group(1)] = m.group(1)
    _PROMPT_MAP_CACHE[key] = out
    return out


def get_sidecar_url(scenario, substyle, image_filename):
    """图对应 sidecar 的 mkdocs 友好 URL(相对画廊所在目录)。无则 None。

    use_directory_urls=True 下 .md 渲染到 dir/index.html,所以去掉 .md 加 trailing /。
    """
    stem = image_filename.rsplit(".", 1)[0]
    md = _get_prompt_map(scenario, substyle).get(stem)
    if not md:
        return None
    md = md.lstrip("./")
    if md.endswith(".md"):
        md = md[:-3] + "/"
    return f"./{md}"


def build_grid(scenario, substyles):
    """场景级 masonry 画廊:点击图开灯箱(glightbox 接管 img)。

    所有 tile 用 <div> 容器,不再跳子分类 README(避免 mkdocs 下 README.md 404)。
    带 sidecar 的图在右上角加 📝 角标,链接到 prompt 页面。
    进入子分类走「可用子分类」清单段。空 substyle 跳过。
    """
    lines = ['<div class="gallery" markdown="0">']
    for s in substyles:
        imgs = collect_images(scenario, s)
        if not imgs:
            continue
        for f in imgs:
            stem = f.rsplit(".", 1)[0]
            src = f"./{s}/{f}"
            sidecar = get_sidecar_url(scenario, s, f)
            lines.append('  <div class="tile">')
            lines.append(f'    <img src="{src}" alt="{_esc(stem)}" loading="lazy">')
            if sidecar:
                # 场景级 sidecar 路径相对场景目录,需拼上 substyle
                sidecar_href = f'./{s}/{sidecar.lstrip("./")}'
                lines.append(f'    <a class="tile-prompt-badge" href="{sidecar_href}" title="查看 prompt">📝</a>')
            lines.append('  </div>')
    lines.append('</div>')
    return "\n".join(lines)


def count_scenario_images(scenario, cfg=None):
    """场景图片总数:有 substyles 时遍历各子目录;扁平场景直接数。"""
    if cfg is not None:
        return sum(
            len(collect_images(scenario, s))
            for s in cfg.get("styles", []) + cfg.get("layouts", [])
        )
    # 扁平 / unclassified
    return len(list_images_in(os.path.join(ROOT, scenario)))


def make_label(filename, prefix, substyle=None):
    """从文件名生成画廊 label。

    - `<prefix>-<substyle>-foo-bar.png` → `foo-bar`(substyle 提供时)
    - `<prefix>-foo.png` → `foo`(扁平场景)
    - 任意以 `-baoyu.<ext>` 结尾的 → `baoyu`(参考示例统一标签)
    """
    stem = filename.rsplit(".", 1)[0]
    if stem.endswith("-baoyu"):
        return "baoyu"
    head = f"{prefix}-{substyle}-" if substyle else f"{prefix}-"
    if stem.startswith(head):
        return stem[len(head):]
    return stem


def build_substyle_gallery(scenario, substyle, prefix):
    """生成子分类 README 画廊段(3 列网格,图链接到自身可看大图)。"""
    return _build_gallery(
        images=collect_images(scenario, substyle),
        path_prefix="./",
        prefix=prefix,
        substyle=substyle,
        scenario=scenario,
    )


def build_flat_scenario_gallery(scenario, prefix):
    """扁平场景 README 画廊段(图直接在场景根目录下)。"""
    files = list_images_in(os.path.join(ROOT, scenario))
    non_baoyu = sorted(f for f in files if not f.endswith("-baoyu.webp"))
    baoyu = sorted(f for f in files if f.endswith("-baoyu.webp"))
    return _build_gallery(
        images=non_baoyu + baoyu,
        path_prefix="./",
        prefix=prefix,
        substyle=None,
        scenario=scenario,
    )


def _build_gallery(images, path_prefix, prefix, substyle, scenario=None):
    """子分类 / 扁平场景画廊:masonry HTML,点击开灯箱(glightbox 接管 img)。

    带 sidecar 的图右上角加 📝 角标,链接到 prompt 页面。
    """
    if not images:
        return "*(暂无图片)*"
    lines = ['<div class="gallery" markdown="0">']
    for f in images:
        stem = f.rsplit(".", 1)[0]
        href = f"{path_prefix}{f}"
        sidecar = get_sidecar_url(scenario, substyle, f) if scenario else None
        lines.append('  <div class="tile">')
        lines.append(f'    <img src="{href}" alt="{_esc(stem)}" loading="lazy">')
        if sidecar:
            lines.append(f'    <a class="tile-prompt-badge" href="{sidecar}" title="查看 prompt">📝</a>')
        lines.append('  </div>')
    lines.append('</div>')
    return "\n".join(lines)


GALLERY_HEAD_RE = re.compile(r"^## 画廊[ \t]*$", re.MULTILINE)
NEXT_H2_RE = re.compile(r"^## ", re.MULTILINE)


def replace_gallery_section(readme_path, new_gallery):
    """在 README 里找 `## 画廊` 锚点,替换标题及其后续内容到下一个 `## ` 标题之前。

    用 head.start() 锚定整段(含标题),保证格式干净不累加。
    """
    if not os.path.isfile(readme_path):
        return False
    with open(readme_path) as f:
        text = f.read()

    head = GALLERY_HEAD_RE.search(text)
    if not head:
        return False

    # 从 `## 画廊` 行之后开始找下一个 `## ` 标题
    after_head = head.end()
    nxt = NEXT_H2_RE.search(text, pos=after_head)
    end = nxt.start() if nxt else len(text)

    rebuilt = (
        "## 画廊\n\n"
        "<!-- 由 scripts/gen_scenario_readmes.py 自动生成,勿手编 -->\n\n"
        + new_gallery.strip()
        + "\n\n"
    )
    new_text = text[:head.start()] + rebuilt + text[end:]
    if new_text == text:
        return False
    with open(readme_path, "w") as f:
        f.write(new_text)
    return True


def update_all_substyle_galleries():
    """脚本化所有子分类 + 扁平场景的画廊段(元数据段不动)。"""
    updated = []

    # 5 个非扁平场景下的子分类
    for scenario, cfg in SCENARIOS.items():
        prefix = cfg["prefix"]
        for substyle in cfg.get("styles", []) + cfg.get("layouts", []):
            d = os.path.join(ROOT, scenario, substyle)
            if not os.path.isdir(d):
                continue
            readme = os.path.join(d, "README.md")
            gallery = build_substyle_gallery(scenario, substyle, prefix)
            if replace_gallery_section(readme, gallery):
                updated.append(os.path.relpath(readme, ROOT))

    # 扁平场景
    for scenario, prefix in FLAT_PREFIXES.items():
        readme = os.path.join(ROOT, scenario, "README.md")
        gallery = build_flat_scenario_gallery(scenario, prefix)
        if replace_gallery_section(readme, gallery):
            updated.append(os.path.relpath(readme, ROOT))

    if updated:
        print(f"updated substyle galleries: {len(updated)} files")
        for p in updated:
            print(f"  · {p}")


def update_root_readme_counts():
    """扫所有场景图片数,替换根 README「场景导航」表最后一列数字。"""
    path = os.path.join(ROOT, "README.md")
    with open(path) as f:
        text = f.read()

    counts = {}
    for scenario, cfg in SCENARIOS.items():
        counts[scenario] = count_scenario_images(scenario, cfg)
    for scenario in FLAT_SCENARIOS + [UNCLASSIFIED]:
        counts[scenario] = count_scenario_images(scenario)

    # 匹配:`| [Anything](./<scenario>/README.md) | desc | sub | NUMBER |`
    for scenario, n in counts.items():
        pattern = re.compile(
            r"(\| \[[^\]]+\]\(\./"
            + re.escape(scenario)
            + r"/README\.md\)[^|\n]*\|[^|\n]*\|[^|\n]*\| )\d+( \|)"
        )
        text, count = pattern.subn(rf"\g<1>{n}\g<2>", text)
        if count == 0:
            print(f"warn: 未在根 README 找到 {scenario} 计数行")

    with open(path, "w") as f:
        f.write(text)
    print(f"updated root README counts: {dict(counts)}")


def gen_scenario_readme(scenario, cfg):
    parts = [
        f"# {cfg['title']} · {cfg['zh']}\n",
        cfg["desc"] + "\n",
        "[← 返回总索引](../README.md)\n",
    ]

    if cfg["styles"]:
        parts.append("## Styles 风格画廊\n")
        parts.append(build_grid(scenario, cfg["styles"]) + "\n")

    if cfg["layouts"]:
        parts.append("## Layouts 布局画廊\n")
        parts.append(build_grid(scenario, cfg["layouts"]) + "\n")

    parts.append("## 可用子分类\n")
    if cfg["styles"]:
        parts.append(
            f"**Styles**({len(cfg['styles'])}):"
            + " · ".join(f"[`{s}`](./{s}/README.md)" for s in cfg["styles"])
        )
    if cfg["layouts"]:
        parts.append(
            f"**Layouts**({len(cfg['layouts'])}):"
            + " · ".join(f"[`{l}`](./{l}/README.md)" for l in cfg["layouts"])
        )

    parts.append(
        "\n> 每张图一格,同一子分类的多张图连续相邻(标签相同即为同组)。"
        "本地收藏图排前、[baoyu-skills](https://github.com/JimLiu/baoyu-skills) "
        "官方示例排后。点任意格跳转到子分类 README 看完整元数据。\n"
    )
    return "\n".join(parts)


def main():
    for scenario, cfg in SCENARIOS.items():
        path = os.path.join(ROOT, scenario, "README.md")
        with open(path, "w") as f:
            f.write(gen_scenario_readme(scenario, cfg))
        print(f"wrote {path}")
    update_all_substyle_galleries()
    update_root_readme_counts()


if __name__ == "__main__":
    main()
