#!/usr/bin/env python3
"""Assemble the self-contained BOB poster HTML from body + style + embedded fonts."""
import pathlib
d = pathlib.Path(__file__).parent
fonts = (d / "fonts.css").read_text()
style = (d / "poster.style.css").read_text()
body  = (d / "poster.body.html").read_text()
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>BOB — A Chatbot, An Agent, Or Both?</title>
<style>
{fonts}
{style}
</style></head>
<body>
{body}
</body></html>
"""
(d / "bob-poster.html").write_text(html)
print("wrote", d / "bob-poster.html", len(html), "bytes")
