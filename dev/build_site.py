#!/usr/bin/env python3
"""Build the website page from the Claude artifact source.

Reads  dev/runestack-artifact.html  (the exact source of the Claude artifact)
Writes index.html at the repo root   (what GitHub Pages serves)

Usage, from anywhere:
  python3 dev/build_site.py <supabase_url> <supabase_publishable_key>

Leave both out to build without a leaderboard. Only ever pass the public
(anon / publishable) key: it ships inside the page for anyone to see."""
import sys, re, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'dev' / 'runestack-artifact.html').read_text(encoding='utf-8')
url = sys.argv[1] if len(sys.argv) > 1 else ''
key = sys.argv[2] if len(sys.argv) > 2 else ''

title = re.search(r'<title>(.*?)</title>', src).group(1)
body = src.replace('<title>' + title + '</title>', '', 1)
cfg = '<script>window.RUNESTACK_CONFIG=' + json.dumps({'supabaseUrl': url, 'supabaseKey': key}) + ';</script>'
reset = ('html{box-sizing:border-box}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
         'body{margin:0}img{max-width:100%}[hidden]{display:none!important}')
html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="theme-color" content="#121420"><title>' + title + '</title>'
        '<style>' + reset + '</style>' + cfg + '</head><body>' + body + '</body></html>')

out = root / 'index.html'
out.write_text(html, encoding='utf-8')
print(out.relative_to(root), len(html), 'bytes; leaderboard', 'ON' if url and key else 'OFF (no keys given)')
