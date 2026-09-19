# -*- coding: utf-8 -*-
"""按修改时间重建首页知识库橱窗（读 notes.json 最新 4 篇）。"""
import datetime
import json
import os
import re

SITE = os.path.dirname(os.path.abspath(__file__))


def main():
    d = json.load(open(os.path.join(SITE, "notes.json"), encoding="utf-8"))
    posts = sorted(d["posts"], key=lambda p: p.get("mtime", 0), reverse=True)
    top = posts[:4]
    lines = []
    for i, p in enumerate(top, 1):
        lines.append(
            '  <a class="recent" href="notes.html#%s"><span class="num">%02d</span>'
            '<span class="t">%s</span><span class="m">知识库 · %s</span></a>'
            % (p["slug"], i, p["title"], p["cat"]))
    block = ('<section id="notes">\n  <div class="sec-h"><h2>知识库</h2><span>/ notes</span></div>\n'
             + "\n".join(lines) + '\n  <a class="more-link" href="notes.html">进入知识库 →</a>\n</section>')
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    idx = re.sub(r'<section id="notes">.*?</section>', lambda _: block, idx, count=1, flags=re.S)
    total = len(d["posts"])
    month = datetime.datetime.now().month
    stat = '<div class="yearstat">2026 \u00b7 已写 <b>%d</b> 篇 \u00b7 更新于 %d 月</div>' % (total, month)
    idx = re.sub(r'<div class="yearstat">.*?</div>', lambda _: stat, idx, count=1)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(idx)
    for p in top:
        print("  [%s] %s" % (p["cat"], p["title"]))
    print("首页橱窗已更新（共 %d 篇）" % total)


if __name__ == "__main__":
    main()
