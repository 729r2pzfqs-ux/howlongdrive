import os
import re

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    old_html = html
    
    # Fix SVGs in h3 tags - add width/height style
    # Match: <h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    html = re.sub(
        r'<h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">',
        '<h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px;vertical-align:middle;margin-right:8px">',
        html
    )
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

# Also EV pages
for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    old_html = html
    html = re.sub(
        r'<h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">',
        '<h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px;vertical-align:middle;margin-right:8px">',
        html
    )
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Fixed h3 SVG icons on {count} pages")
