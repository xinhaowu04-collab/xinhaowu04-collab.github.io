# -*- coding: utf-8 -*-
"""按修改时间重建首页知识库橱窗：最新更新的 4 篇笔记排最前。
用法：python gen_home.py（在 gen_notes.py 之后运行）
"""
import datetime
import os
import re

SITE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(SITE, "notes")
CAT_NAMES = {
    "c-re": "C 逆向", "pe": "PE 结构", "asm32": "32 位汇编", "asm16": "16 位汇编",
    "dbg": "调试器", "pack": "壳与脱壳", "cpp-re": "C++ 逆向",
    "fx": "实战方法论", "tpl": "模板",
}

def main():
    pages = []
    for f in os.listdir(NOTES):
        if not f.endswith(".html"):
            continue
        path = os.path.join(NOTES, f)
        html = open(path, encoding="utf-8").read()
        m = re.search(r"<title>(.*?) · 0xL</title>", html)
        title = m.group(1) if m else f[:-5]
        slug = f.split("-")[0] if "-" in f else f
        # 复合 slug（c-re、cpp-re）
        if f.startswith("c-re-") or f.startswith("cpp-re-"):
            slug = f.rsplit("-", 1)[0].rsplit("-", 1)[0] if False else ("c-re" if f.startswith("c-re-") else "cpp-re")
        cat = CAT_NAMES.get(slug, "知识库")
        pages.append((os.path.getmtime(path), f, title, cat))

    pages.sort(reverse=True)
    top = pages[:4]

    lines = []
    for i, (_, f, title, cat) in enumerate(top, 1):
        lines.append(
            '  <a class="recent" href="notes/%s"><span class="num">%02d</span>'
            '<span class="t">%s</span><span class="m">知识库 · %s</span></a>' % (f, i, title, cat)
        )
    block = '<section id="notes">\n  <div class="sec-h"><h2>知识库</h2><span>/ notes</span></div>\n' + \
            "\n".join(lines) + '\n  <a class="more-link" href="notes.html">进入知识库 →</a>\n</section>'

    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    new_idx = re.sub(r'<section id="notes">.*?</section>', lambda _: block, idx, count=1, flags=re.S)
    # 年度统计：笔记总数 + 当前月份
    total = len([f for f in os.listdir(NOTES) if f.endswith(".html")])
    month = datetime.datetime.now().month
    stat = '<div class="yearstat">2026 \u00b7 已写 <b>%d</b> 篇 \u00b7 更新于 %d 月</div>' % (total, month)
    new_idx = re.sub(r'<div class="yearstat">.*?</div>', lambda _: stat, new_idx, count=1)
    # 年度统计：笔记总数 + 当前月份
    total = len([f for f in os.listdir(NOTES) if f.endswith(".html")])
    month = datetime.datetime.now().month
    stat = '<div class="yearstat">2026 · 已写 <b>%d</b> 篇 · 更新于 %d 月</div>' % (total, month)
    new_idx = re.sub(r'<div class="yearstat">.*?</div>', lambda _: stat, new_idx, count=1)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(new_idx)
    for _, f, title, cat in top:
        print("  [%s] %s" % (cat, title))
    print("首页知识库橱窗已按最新更新排序")


if __name__ == "__main__":
    main()
