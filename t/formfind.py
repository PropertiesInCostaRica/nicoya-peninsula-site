#!/usr/bin/env python3
# Read only. Finds the form handlers that still send mail "From" the visitor's
# own address (this is what Gmail rejects for yahoo/aol/hotmail visitors).
import os, re
ROOT = '/var/www/propertiesincostarica.com/web'
SKIP = ('/blog/wp-', '/node_modules/', '/.git/')
pages, handlers = [], []
for d, _, fs in os.walk(ROOT):
    if any(s in d + '/' for s in SKIP):
        continue
    for f in fs:
        if not f.endswith(('.php', '.html', '.htm', '.inc')):
            continue
        p = os.path.join(d, f)
        try:
            t = open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        if f.endswith(('.html', '.htm')):
            if 'List Your Property with Us' in t and '<form' in t:
                acts = re.findall(r'<form[^>]*action="([^"]*)"', t)
                pages.append((p, acts))
            continue
        if re.search(r'\bmail\s*\(|PHPMailer|->setFrom|->From\b', t):
            lines = []
            for i, l in enumerate(t.split('\n'), 1):
                if re.search(r'From:|setFrom|->From\b|Reply-To|addReplyTo|\bmail\s*\(|Mail Request', l):
                    lines.append('   %d: %s' % (i, l.strip()[:160]))
            handlers.append((p, lines))
print('@@ Pages with the List Your Property form (first 5):')
for p, a in pages[:5]:
    print('  ', p.replace(ROOT, ''), '-> action:', a)
print('@@ Total pages with it:', len(pages))
print('@@ PHP files that send mail:')
for p, ls in handlers:
    print(' FILE', p.replace(ROOT, ''))
    for l in ls[:12]:
        print(l)
