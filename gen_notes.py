# -*- coding: utf-8 -*-
"""把 Obsidian 笔记（Markdown）转成站内笔记页。
用法：python gen_notes.py <md目录> <分类slug> <分类中文名>
例：python gen_notes.py "C:\\Users\\Lenovo\\Desktop\\科锐三阶段笔记\\c逆向" c-re "C 逆向"
输出：personal-site/notes/<slug>-XX.html + 打印每篇标题（供首页索引用）
"""
import html
import os
import re
import sys

SITE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 0xL</title>
<script>window.MathJax = {{ tex: {{ inlineMath: [['$','$']] }} }};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
:root {{ --bg:#fdfbf9; --card:#fff; --border:#f0e8e4; --text:#3a3a44; --dim:#9c96a3; --pink:#f08fb7; --pink-deep:#e56aa0; --shadow:0 6px 24px rgba(229,106,160,.08); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--text); font-family:"PingFang SC","Microsoft YaHei",sans-serif; line-height:1.9; }}
.wrap {{ max-width:760px; margin:0 auto; padding:28px 24px 80px; }}
a.back {{ color:var(--pink-deep); text-decoration:none; font-size:14px; }}
a.back:hover {{ text-decoration:underline; }}
h1.title {{ font-size:26px; margin:18px 0 6px; }}
.meta {{ color:var(--dim); font-size:13px; margin-bottom:28px; }}
.meta .cat {{ color:var(--pink-deep); background:rgba(240,143,183,.12); padding:2px 10px; border-radius:999px; }}
article {{ background:var(--card); border:1px solid var(--border); border-radius:18px; box-shadow:var(--shadow); padding:34px 36px; }}
article h1,article h2,article h3,article h4 {{ margin:1.4em 0 .6em; line-height:1.5; }}
article h1 {{ font-size:22px }} article h2 {{ font-size:20px }} article h3 {{ font-size:17px }} article h4 {{ font-size:15px; color:var(--pink-deep) }}
article p {{ margin:.6em 0; }}
article ul,article ol {{ margin:.6em 0 .6em 1.6em; }}
article code {{ font-family:Consolas,monospace; font-size:.92em; background:rgba(240,143,183,.1); color:#c2377c; padding:1px 6px; border-radius:6px; }}
article pre {{ background:#2b2b36; color:#e8e8f0; border-radius:12px; padding:16px 18px; overflow-x:auto; margin:.8em 0; }}
article pre code {{ background:none; color:inherit; padding:0; }}
article blockquote {{ border-left:3px solid var(--pink); padding-left:14px; color:var(--dim); margin:.8em 0; }}
article img {{ max-width:100%; border-radius:12px; }}
article table {{ border-collapse:collapse; margin:.8em 0; width:100%; }}
article th,article td {{ border:1px solid var(--border); padding:8px 12px; font-size:14px; }}
article th {{ background:rgba(240,143,183,.08); }}
hr {{ border:none; border-top:1px solid var(--border); margin:1.4em 0; }}
  background:url("../penguin.png") center/contain no-repeat;
  filter:drop-shadow(0 2px 3px rgba(0,0,0,.15));
</style>
</head>
<body>
<div class="wrap">
<a class="back" href="javascript:history.back()">← 返回</a>
<h1 class="title">{title}</h1>
<div class="meta"><span class="cat">{cat}</span></div>
<article>
{body}
</article>
</div>
<script>
document.addEventListener('mousemove', function (e) {{ mx = e.clientX; my = e.clientY; }});
(function loop() {{ dot.style.left = mx + 'px'; dot.style.top = my + 'px'; requestAnimationFrame(loop); }})();
document.querySelectorAll('a').forEach(function (el) {{
  el.addEventListener('mouseenter', function () {{ dot.classList.add('hov'); }});
  el.addEventListener('mouseleave', function () {{ dot.classList.remove('hov'); }});
}});
</script>
</body>
</html>
"""


def md_to_html(md):
    lines = md.split("\n")
    out, in_code, in_list, in_math, para = [], False, False, False, []

    def flush_para():
        if para:
            out.append("<p>" + " ".join(para) + "</p>")
            para.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            flush_para(); close_list()
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        s = line.strip()
        if s.startswith("$$"):
            flush_para(); close_list()
            if not in_math:
                out.append('<div class="math">$$')
                in_math = True
            else:
                out.append('$$</div>')
                in_math = False
            continue
        if in_math:
            out.append(s)
            continue
        if not s:
            flush_para(); close_list()
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush_para(); close_list()
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, m.group(2), lv))
            continue
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>%s</li>" % m.group(1))
            continue
        if s.startswith("> "):
            flush_para(); close_list()
            out.append("<blockquote>%s</blockquote>" % s[2:])
            continue
        if s == "---":
            flush_para(); close_list()
            out.append("<hr>")
            continue
        close_list()
        para.append(s)
    flush_para(); close_list()
    body = "\n".join(out)
    # 行内样式
    body = re.sub(r"`([^`]+)`", r"<code>\1</code>", body)
    body = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", body)
    return body


def get_title(md, fallback):
    for line in md.split("\n"):
        m = re.match(r"^#{1,6}\s+(.+)$", line.strip())
        if m:
            t = m.group(1).strip()
            t = re.sub(r"[`*_]+", "", t).strip(" ：:").strip()
            return t[:40] if t else fallback
    return fallback


def main():
    src, slug, cat = sys.argv[1], sys.argv[2], sys.argv[3]
    outdir = os.path.join(SITE, "notes")
    os.makedirs(outdir, exist_ok=True)
    entries = []
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".md"):
            continue
        md = open(os.path.join(src, fn), encoding="utf-8").read()
        num = fn[:-3]
        # 纯数字文件名取正文首个标题；否则用文件名本身
        if num.isdigit():
            title = get_title(md, "%s %s" % (cat, num))
        else:
            title = num
        page = "%s-%s.html" % (slug, num)
        with open(os.path.join(outdir, page), "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(title=title, cat=cat, body=md_to_html(md)))
        entries.append((page, title))
        print("%s|%s" % (page, title))
    print("共生成 %d 篇" % len(entries))


if __name__ == "__main__":
    main()
