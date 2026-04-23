#!/usr/bin/env python3
"""生成场景 README:3 列大网格平铺,每子分类一张封面;本地图优先作封面。"""
import os

ROOT = "/Users/maozhenshou/Documents/AICode/image-seed"

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


def collect_images(scenario, substyle):
    """该子分类下所有图,本地图优先,baoyu 排最后。"""
    d = os.path.join(ROOT, scenario, substyle)
    if not os.path.isdir(d):
        return []
    files = [f for f in os.listdir(d)
             if f != "README.md" and os.path.isfile(os.path.join(d, f))]
    non_baoyu = sorted(f for f in files if not f.endswith("-baoyu.webp"))
    baoyu = sorted(f for f in files if f.endswith("-baoyu.webp"))
    return non_baoyu + baoyu


def build_grid(scenario, substyles):
    """平铺 3 列网格:每张图占一格,同子分类连续相邻。"""
    tiles = []  # list of (substyle, filename or None)
    for s in substyles:
        imgs = collect_images(scenario, s)
        if not imgs:
            tiles.append((s, None))
        else:
            for f in imgs:
                tiles.append((s, f))

    lines = ["|   |   |   |", "|:---:|:---:|:---:|"]
    cols = 3
    for i in range(0, len(tiles), cols):
        group = tiles[i:i + cols]
        img_cells = []
        label_cells = []
        for (s, f) in group:
            if f is None:
                img_cells.append("*(暂无)*")
            else:
                img_cells.append(f"[![{s}](./{s}/{f})](./{s}/README.md)")
            label_cells.append(f"[{s}](./{s}/README.md)")
        while len(img_cells) < cols:
            img_cells.append("  ")
            label_cells.append("  ")
        lines.append("| " + " | ".join(img_cells) + " |")
        lines.append("| " + " | ".join(label_cells) + " |")
    return "\n".join(lines)


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


if __name__ == "__main__":
    main()
