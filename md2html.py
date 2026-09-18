"""Convert a markdown tutorial to a single self-contained HTML file.

Usage: python md2html.py input.md [output.html]

Local images are embedded as base64 so the file can be shared via
chat tools (DingTalk/WeChat) without a folder.
"""
import base64
import mimetypes
import pathlib
import re
import sys

import markdown

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script>
MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }} }};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
body {{
  font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
  max-width: 860px; margin: 0 auto; padding: 24px 16px;
  line-height: 1.75; color: #24292f;
}}
h1, h2 {{ border-bottom: 2px solid #d0d7de; padding-bottom: 8px; }}
h1 {{ font-size: 1.7em; }}
h2 {{ font-size: 1.35em; margin-top: 1.6em; }}
img {{ max-width: 100%; display: block; margin: 12px auto; }}
table {{ border-collapse: collapse; margin: 16px 0; }}
th, td {{ border: 1px solid #d0d7de; padding: 6px 14px; }}
th {{ background: #f6f8fa; }}
code {{ background: #f6f8fa; padding: 2px 5px; border-radius: 4px; }}
pre code {{ display: block; padding: 12px; overflow-x: auto; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def embed_local_images(html: str, base_dir: pathlib.Path) -> str:
    def repl(m):
        attrs, src, tail = m.groups()
        if re.match(r"^(https?:|data:)", src):
            return m.group(0)
        path = (base_dir / src).resolve()
        if not path.is_file():
            print(f"WARNING: image not found: {src}")
            return m.group(0)
        mime = mimetypes.guess_type(path.name)[0] or "image/png"
        data = base64.b64encode(path.read_bytes()).decode()
        return f'<img {attrs}src="data:{mime};base64,{data}"{tail}>'

    return re.sub(r'<img ([^>]*?)src="([^"]+)"([^>]*?)>', repl, html)


def main():
    src = pathlib.Path(sys.argv[1]).resolve()
    dst = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else src.with_suffix(".html")

    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    body = embed_local_images(body, src.parent)

    dst.write_text(TEMPLATE.format(title=src.stem, body=body), encoding="utf-8")
    print(f"OK: {dst} ({dst.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
