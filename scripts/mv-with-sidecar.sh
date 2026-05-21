#!/usr/bin/env bash
# 一次性搬迁图片 + 同 trunk 的 sidecar (.md)。
#
# 用法:
#   scripts/mv-with-sidecar.sh <src-no-ext> <dst-no-ext>
#
# 例:
#   scripts/mv-with-sidecar.sh unclassified/1 \
#     infographic/craft-handmade/info-craft-handmade-fourier-transform
#
# 支持两种 sidecar 关联:
#   (a) 同 basename: 1.jpg ↔ 1.md(单图情形)
#   (b) 同 trunk:    2-0.jpeg / 2-1.jpeg / ... ↔ 2.md(多变体共享 prompt)
#
# 算法:
#   1. 先找同 basename .md;
#   2. 没有则找 trunk .md(trunk = basename 去掉 `-N`/`-NN`/`-NNN` 后缀);
#   3. trunk 情形下,sidecar 搬到目标 trunk(后续变体跑同脚本会探测到 trunk sidecar
#      已在目标位置,自动跳过,实现"第一张图带 sidecar、后续变体共用")
#
# 自动识别图片扩展名(.jpg .jpeg .png .webp .gif),已存在目标拒绝覆盖。

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "用法: $0 <src-no-ext> <dst-no-ext>" >&2
  echo "  src/dst 都不含扩展名;脚本自己探测 .jpg/.png/.webp/.jpeg/.gif" >&2
  exit 2
fi

SRC="$1"
DST="$2"

# 找图片扩展名
SRC_IMG=""
SRC_EXT=""
for ext in jpg jpeg png webp gif JPG JPEG PNG WEBP GIF; do
  if [[ -f "${SRC}.${ext}" ]]; then
    SRC_IMG="${SRC}.${ext}"
    SRC_EXT="${ext}"
    break
  fi
done

if [[ -z "${SRC_IMG}" ]]; then
  echo "错误:找不到图片 ${SRC}.{jpg,jpeg,png,webp,gif}" >&2
  exit 1
fi

DST_IMG="${DST}.${SRC_EXT}"
DST_DIR="$(dirname "${DST_IMG}")"

if [[ ! -d "${DST_DIR}" ]]; then
  echo "错误:目标目录不存在: ${DST_DIR}" >&2
  exit 1
fi

if [[ -e "${DST_IMG}" ]]; then
  echo "错误:目标已存在,拒绝覆盖: ${DST_IMG}" >&2
  exit 1
fi

# 计算 trunk(去掉 `-数字` 后缀)
SRC_TRUNK="$(echo "${SRC}" | sed -E 's/-[0-9]+$//')"
DST_TRUNK="$(echo "${DST}" | sed -E 's/-[0-9]+$//')"

# 探测 sidecar(优先同 basename,其次同 trunk)
SIDECAR_SRC=""
SIDECAR_DST=""
if [[ -f "${SRC}.md" ]]; then
  SIDECAR_SRC="${SRC}.md"
  SIDECAR_DST="${DST}.md"
elif [[ "${SRC}" != "${SRC_TRUNK}" && -f "${SRC_TRUNK}.md" ]]; then
  SIDECAR_SRC="${SRC_TRUNK}.md"
  SIDECAR_DST="${DST_TRUNK}.md"
fi

# 搬图
mv "${SRC_IMG}" "${DST_IMG}"
echo "moved image: ${SRC_IMG} → ${DST_IMG}"

# 搬 sidecar(若找到)
if [[ -n "${SIDECAR_SRC}" ]]; then
  if [[ -e "${SIDECAR_DST}" ]]; then
    echo "(sidecar 目标已存在 ${SIDECAR_DST},跳过 —— 多变体共享 sidecar 时正常)" >&2
  else
    mv "${SIDECAR_SRC}" "${SIDECAR_DST}"
    echo "moved sidecar: ${SIDECAR_SRC} → ${SIDECAR_DST}"
  fi
else
  echo "(未找到 sidecar,跳过)"
fi
