import os

FAQ_CSS = '''
        .faq { margin-top: 1.5rem; }
        .faq h2 { font-size: 1.1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
        .faq h2 svg { width: 20px; height: 20px; color: var(--primary); }
        .faq-item { background: var(--card); border-radius: 0.5rem; margin-bottom: 0.75rem; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .faq-q { font-weight: 600; padding: 1rem 1.25rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; }
        .faq-q:hover { background: #f8fafc; }
        .faq-q svg { width: 16px; height: 16px; color: var(--muted); transition: transform 0.2s; }
        .faq-item.open .faq-q svg { transform: rotate(180deg); }
        .faq-a { padding: 0 1.25rem 1rem; font-size: 0.875rem; color: var(--muted); display: none; }
        .faq-item.open .faq-a { display: block; }'''

count = 0
for root, dirs, files in os.walk('route'):
    for f in files:
        if f != 'index.html':
            continue
        path = os.path.join(root, f)
        with open(path) as file:
            html = file.read()
        
        # Add FAQ CSS if page has FAQ but not styles
        if 'class="faq"' in html and '.faq-item' not in html:
            html = html.replace('</style>', FAQ_CSS + '\n    </style>')
            with open(path, 'w') as file:
                file.write(html)
            count += 1

print(f"✅ Added FAQ styles to {count} pages")
