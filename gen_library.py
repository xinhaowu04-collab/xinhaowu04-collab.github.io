# -*- coding: utf-8 -*-
"""把 Obsidian 笔记库全量编译成 notes.json（知识库数据文件）。
用法：python gen_library.py
分类清单写死在 CATS 里，新增分类加一行即可。
"""
import datetime
import json
import os
import re

SITE = os.path.dirname(os.path.abspath(__file__))
VAULT = r"C:\Users\Lenovo\Desktop\科锐三阶段笔记"

CATS = [
    (VAULT + r"\c逆向", "c-re", "C 逆向"),
    (VAULT + r"\PE", "pe", "PE 结构"),
    (VAULT + r"\32位汇编", "asm32", "32 位汇编"),
    (VAULT + r"\16位汇编", "asm16", "16 位汇编"),
    (VAULT + r"\调试器", "dbg", "调试器"),
    (VAULT + r"\壳", "pack", "壳与脱壳"),
    (VAULT + r"\c++逆向", "cpp-re", "C++ 逆向"),
]
EXTRA = [  # 单独文件（模板、方法论等）
    (os.path.join(SITE, "md", "实战写作模板.md"), "tpl", "模板"),
    (VAULT + r"\病毒分析公式化打法.md", "fx", "实战方法论"),
]
SKIP = ("考卷", "答案")


def get_title(md, fallback):
    for line in md.splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            return line
    return fallback


def main():
    posts = []
    for src, slug, cat in CATS:
        if not os.path.isdir(src):
            print("跳过（目录不存在）:", src)
            continue
        for fn in sorted(os.listdir(src)):
            if not fn.endswith(".md") or any(s in fn for s in SKIP):
                continue
            path = os.path.join(src, fn)
            md = open(path, encoding="utf-8").read()
            num = fn[:-3]
            title = get_title(md, num) if num.isdigit() else num
            posts.append({
                "slug": "%s-%s" % (slug, num),
                "title": title,
                "cat": cat,
                "body": md,
                "mtime": os.path.getmtime(path),
            })
    for path, slug, cat in EXTRA:
        if not os.path.exists(path):
            continue
        md = open(path, encoding="utf-8").read()
        posts.append({
            "slug": "%s-%s" % (slug, os.path.basename(path)[:-3]),
            "title": get_title(md, os.path.basename(path)[:-3]),
            "cat": cat,
            "body": md,
            "mtime": os.path.getmtime(path),
        })

    out = {"generated": datetime.datetime.now().isoformat(timespec="seconds"), "posts": posts}
    with open(os.path.join(SITE, "notes.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print("notes.json 生成，共 %d 篇" % len(posts))


if __name__ == "__main__":
    main()
