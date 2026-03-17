import os
import re

pin_svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:28px;height:28px;vertical-align:middle;margin-right:8px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'
bolt_svg = '⚡'  # Keep in EV badge, it's fine

count = 0
for d in os.listdir('cities'):
    if not os.path.isdir(f'cities/{d}'):
        continue
    path = f'cities/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    changed = False
    
    # Remove HowLongDrive text from logo
    if 'alt="HowLongDrive">HowLongDrive</a>' in html:
        html = html.replace('alt="HowLongDrive">HowLongDrive</a>', 'alt="HowLongDrive"></a>')
        changed = True
    
    # Replace pin emoji in h1
    if '<h1>📍' in html:
        html = html.replace('<h1>📍', f'<h1>{pin_svg}')
        changed = True
    
    if changed:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Fixed {count} city pages")
