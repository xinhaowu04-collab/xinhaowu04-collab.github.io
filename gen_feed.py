# -*- coding: utf-8 -*-
"""从 notes/ 目录自动生成 RSS feed.xml。
用法：python gen_feed.py
标题从每个 html 的 <title> 提取（'标题 · 0xL' 格式）。
"""
import datetime
import os
import re

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://xinhaowu04-collab.github.io"

def main():
    notes_dir = os.path.join(SITE, "notes")
    items = []
    for fn in sorted(os.listdir(notes_dir)):
        if not fn.endswith(".html"):
            continue
        html = open(os.path.join(notes_dir, fn), encoding="utf-8").read()
        m = re.search(r"<title>(.*?) · 0xL</title>", html)
        title = m.group(1) if m else fn[:-5]
        items.append((fn, title))

    now = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">', '<channel>',
        '<title>0xL · 逆向练习生</title>',
        '<link>%s</link>' % BASE,
        '<description>二进制世界的探险笔记</description>',
        '<language>zh-CN</language>',
        '<lastBuildDate>%s</lastBuildDate>' % now,
    ]
    for fn, title in items:
        lines.append('<item><title>%s</title><link>%s/notes/%s</link></item>' % (title, BASE, fn))
    lines += ['</channel>', '</rss>', '']

    out = os.path.join(SITE, "feed.xml")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print("feed.xml 已生成，共 %d 条" % len(items))


if __name__ == "__main__":
    main()
