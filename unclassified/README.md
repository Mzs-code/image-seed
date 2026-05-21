# Unclassified · 未分类

待归档图片的缓冲区。详细规则见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

**真相源**:`ls unclassified/` —— 本 README 不再维护画廊(暂存物会经常变,手维护必脱钩)。

**投递(入库)**:
1. 图片丢入本目录,**文件名尽量带语义(`fourier-transform-poster.jpg`)而非顺序号(`1.jpg`)**,避免命名冲突
2. **若有 prompt → 同时建同 trunk 的 sidecar**:`fourier-transform-poster.jpg` ↔ `fourier-transform-poster.md`。一个 prompt 对应多张变体:图片命名为 `<trunk>-01.png` / `<trunk>-02.png`、sidecar 只一份 `<trunk>.md`(详见 [Prompt sidecar 文件](../CONTRIBUTING.md#prompt-sidecar-文件))

**归类(出库)**:
1. 确定目标场景 + 子分类
2. **推荐用 `scripts/mv-with-sidecar.sh <src-no-ext> <dst-no-ext>`**:一次搬图 + sidecar,不会脱钩
   ```bash
   scripts/mv-with-sidecar.sh unclassified/fourier-transform-poster infographic/craft-handmade/info-craft-handmade-fourier-transform
   ```
   不用脚本时,普通 `mv`(暂存文件未 `git add`,`git mv` 会失败);务必检查同 trunk 的 `.md` 也搬走了
3. 更新目标子分类 README 画廊 + 元数据行
4. 跑 `python3 scripts/gen_scenario_readmes.py`(同步场景 README + 根 README 数字)

[← 返回总索引](../README.md)
