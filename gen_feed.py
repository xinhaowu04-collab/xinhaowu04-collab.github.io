# -*- coding: utf-8 -*-
"""从 notes.json 生成 RSS feed.xml。"""
import datetime
import json
import os

SITE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://0xl.top"


def main():
    d = json.load(open(os.path.join(SITE, "notes.json"), encoding="utf-8"))
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
    for p in d["posts"]:
        lines.append('<item><title>%s</title><link>%s/notes.html#%s</link></item>' % (p["title"], BASE, p["slug"]))
    lines += ['</channel>', '</rss>', '']
    open(os.path.join(SITE, "feed.xml"), "w", encoding="utf-8").write("\n".join(lines))
    print("feed.xml 已生成，共 %d 条" % len(d["posts"]))


if __name__ == "__main__":
    main()
