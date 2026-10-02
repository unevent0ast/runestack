#!/usr/bin/env python3
"""Turn runestack.html (the Claude artifact) into site/index.html for regular web hosting.
Usage: python3 build_site.py [supabase_url] [supabase_key]"""
import sys,re,json
src=open('runestack.html').read()
url=sys.argv[1] if len(sys.argv)>1 else ''
key=sys.argv[2] if len(sys.argv)>2 else ''
title=re.search(r'<title>(.*?)</title>',src).group(1)
body=src.replace('<title>'+title+'</title>','',1)
cfg='<script>window.RUNESTACK_CONFIG='+json.dumps({'supabaseUrl':url,'supabaseKey':key})+';</script>'
reset=('html{box-sizing:border-box}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
       'body{margin:0}img{max-width:100%}[hidden]{display:none!important}')
html=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<meta name="theme-color" content="#121420"><title>'+title+'</title>'
      '<style>'+reset+'</style>'+cfg+'</head><body>'+body+'</body></html>')
open('site/index.html','w').write(html)
print('site/index.html',len(html),'bytes; leaderboard','ON' if url and key else 'OFF (no keys yet)')
