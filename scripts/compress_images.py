#!/usr/bin/env python3
"""压缩超标 PNG/JPG → WebP,自动改同目录 README 引用。

用法:
  scripts/compress_images.py <path>                         # 处理目录递归
  scripts/compress_images.py <path> --threshold-kb 500      # 阈值改 500KB
  scripts/compress_images.py <path> --dry-run               # 只看不动
  scripts/compress_images.py <path> --keep-original         # 留原图便于对比
  scripts/compress_images.py <path> --quality 90            # 提高质量(默认 85)

行为:
  1. 递归扫指定路径下所有 .png/.jpg/.jpeg
  2. 跳过 ≤ threshold-kb 的图(默认 1024 KB = 1 MB)
  3. PNG/JPG → WebP(同目录、同 basename、改后缀)
  4. 默认删原图;同步替换该目录 README.md 里 `<oldname>.png` → `<oldname>.webp`
  5. 完成后提示跑 gen_scenario_readmes.py 让画廊重生成

注意:
  - 不动 .webp(已经是 WebP)
  - 不动 < 阈值 的图(基本已经压过)
  - 转换后建议人眼复核 2-3 张观感,有损伤就 --quality 90 重做
"""
import argparse
import os
import sys
from PIL import Image

SRC_EXTS = (".png", ".jpg", ".jpeg")


def compress_one(src, dst, quality, method):
    img = Image.open(src)
    # 处理特殊 mode
    if img.mode == "P":
        img = img.convert("RGBA") if "transparency" in img.info else img.convert("RGB")
    elif img.mode == "CMYK":
        img = img.convert("RGB")
    save_kwargs = {"quality": quality, "method": method}
    img.save(dst, "WEBP", **save_kwargs)


def find_repo_root(path):
    """从给定路径上溯找 .git 目录所在,作为仓库根。"""
    p = os.path.abspath(path)
    while p != os.path.dirname(p):
        if os.path.isdir(os.path.join(p, ".git")):
            return p
        p = os.path.dirname(p)
    return None


_REPO_MD_CACHE = None


def _all_md_files(repo_root):
    global _REPO_MD_CACHE
    if _REPO_MD_CACHE is not None:
        return _REPO_MD_CACHE
    found = []
    for root, dirs, files in os.walk(repo_root):
        # 跳过 site / .git / .venv
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("site", "node_modules")]
        for f in files:
            if f.endswith(".md"):
                found.append(os.path.join(root, f))
    _REPO_MD_CACHE = found
    return found


def update_references(repo_root, old_name, new_name):
    """跨全仓 .md 文件替换 `old_name` → `new_name`,返回被改的文件列表。"""
    updated = []
    for p in _all_md_files(repo_root):
        with open(p) as f:
            text = f.read()
        if old_name not in text:
            continue
        new_text = text.replace(old_name, new_name)
        with open(p, "w") as f:
            f.write(new_text)
        updated.append(os.path.relpath(p, repo_root))
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", help="目录或文件路径")
    parser.add_argument("--quality", type=int, default=85, help="WebP 质量 (0-100, 默认 85)")
    parser.add_argument("--method", type=int, default=6, help="WebP 编码 effort (0-6, 默认 6 最佳)")
    parser.add_argument("--threshold-kb", type=int, default=1024,
                        help="只压 > 此 KB 的图(默认 1024)")
    parser.add_argument("--dry-run", action="store_true", help="只列出不实际操作")
    parser.add_argument("--keep-original", action="store_true", help="保留原图(默认删除)")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    # 收集目标文件
    targets = []
    if os.path.isfile(args.path):
        targets = [args.path]
    else:
        for root, dirs, files in os.walk(args.path):
            # 跳过 site/ / .venv* / .git / 隐藏目录(构建产物 / 依赖)
            dirs[:] = [d for d in dirs
                       if not d.startswith(".")
                       and d not in ("site", "node_modules", "__pycache__")]
            for f in files:
                if not f.lower().endswith(SRC_EXTS):
                    continue
                p = os.path.join(root, f)
                if os.path.getsize(p) >= args.threshold_kb * 1024:
                    targets.append(p)

    targets.sort(key=lambda p: -os.path.getsize(p))
    if not targets:
        print(f"没找到 > {args.threshold_kb} KB 的可压图")
        return

    print(f"找到 {len(targets)} 张超标图(> {args.threshold_kb} KB)")
    print(f"参数: quality={args.quality}, method={args.method}, "
          f"{'dry-run' if args.dry_run else '保留原图' if args.keep_original else '删原图 + 改 README'}")
    print()

    total_before = 0
    total_after = 0
    converted = 0
    skipped = 0
    failed = 0

    for src in targets:
        before = os.path.getsize(src)
        total_before += before
        stem, _ = os.path.splitext(src)
        dst = stem + ".webp"

        if os.path.exists(dst):
            print(f"  SKIP  {src}  ({before/1024/1024:.2f} MB,目标 .webp 已存在)")
            skipped += 1
            total_after += before
            continue

        if args.dry_run:
            print(f"  [dry] {src}  ({before/1024/1024:.2f} MB → would convert)")
            continue

        try:
            compress_one(src, dst, args.quality, args.method)
        except Exception as e:
            print(f"  FAIL  {src}: {e}")
            failed += 1
            total_after += before
            continue

        after = os.path.getsize(dst)
        total_after += after
        red = (before - after) / before * 100

        suffix = ""
        if not args.keep_original:
            old_name = os.path.basename(src)
            new_name = os.path.basename(dst)
            repo_root = find_repo_root(src)
            if repo_root:
                updated = update_references(repo_root, old_name, new_name)
                suffix = f"  [改了 {len(updated)} 个 .md]" if updated else "  [没找到引用]"
            else:
                suffix = "  [未找到仓库根]"
            os.remove(src)

        print(f"  {before/1024/1024:5.2f} → {after/1024/1024:4.2f} MB  ({red:2.0f}% ↓)  {src}{suffix}")
        converted += 1

    print()
    if args.dry_run:
        print(f"[dry-run] {len(targets)} 张图待压,总 {total_before/1024/1024:.1f} MB")
    else:
        saved = total_before - total_after
        print(f"完成:转换 {converted} / 跳过 {skipped} / 失败 {failed}")
        if converted:
            print(f"总计:{total_before/1024/1024:.1f} MB → {total_after/1024/1024:.1f} MB  "
                  f"减重 {saved/1024/1024:.1f} MB ({saved/total_before*100:.0f}%)")
            print()
            print("下一步:跑 `python3 scripts/gen_scenario_readmes.py` 同步场景画廊 + 数字")


if __name__ == "__main__":
    main()
