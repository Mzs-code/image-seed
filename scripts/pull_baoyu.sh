#!/usr/bin/env bash
# 从 baoyu-skills 仓库拉取所有 7 组示例图到本地对应子分类目录。
#
# 使用场景:
#   - 首次初始化:下载 82 张官方示例作为参考封面
#   - baoyu-skills 仓库更新后重新同步
#
# 注意:
#   - 覆盖已有的 `<prefix>-<substyle>-baoyu.webp`,不覆盖本地非 baoyu 图
#   - 如果已知某个 substyle 的本地图就是 baoyu 示例(见 CLAUDE.md 去重规则),
#     跑完后要手动删除对应的 -baoyu.webp
#
# 已知去重清单(跑完需处理):
#   - slide-deck/sketch-notes/ (deck-sketch-notes-how-ai-learns.jpg 即是 baoyu 示例)

set -e
BASE=https://raw.githubusercontent.com/JimLiu/baoyu-skills/main/screenshots
ROOT=$(cd "$(dirname "$0")/.." && pwd)

dl() {
  local baoyu_cat=$1 scenario=$2 prefix=$3
  shift 3
  for name in "$@"; do
    mkdir -p "$ROOT/$scenario/$name"
    curl -fsSL --retry 3 "$BASE/$baoyu_cat/$name.webp" \
      -o "$ROOT/$scenario/$name/$prefix-$name-baoyu.webp"
  done
}

dl xhs-images-styles xhs-images xhs \
  cute fresh warm bold minimal retro pop notion chalkboard
dl xhs-images-layouts xhs-images xhs \
  sparse balanced dense list comparison flow
dl infographic-styles infographic info \
  craft-handmade claymation kawaii storybook-watercolor chalkboard \
  cyberpunk-neon bold-graphic aged-academia corporate-memphis \
  technical-schematic origami pixel-art ui-wireframe subway-map \
  ikea-manual knolling lego-brick
dl infographic-layouts infographic info \
  bridge circular-flow comparison-table do-dont equation feature-list \
  fishbone funnel grid-cards iceberg journey-path layers-stack \
  mind-map nested-circles priority-quadrants pyramid scale-balance \
  timeline-horizontal tree-hierarchy venn
dl slide-deck-styles slide-deck deck \
  blueprint chalkboard bold-editorial corporate dark-atmospheric \
  editorial-infographic fantasy-animation intuition-machine minimal \
  notion pixel-art scientific sketch-notes vector-illustration \
  vintage watercolor
dl comic-layouts comic comic \
  standard cinematic dense splash mixed webtoon
dl article-illustrator-styles article-illustrator art \
  notion elegant warm minimal blueprint watercolor editorial scientific

echo "downloaded: $(find "$ROOT" -name '*-baoyu.webp' | wc -l) files"
