import os

CAR_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:28px;height:28px;vertical-align:middle;margin-right:8px"><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M5 17H3v-6l2-5h10l2 5v6h-2M5 17h10"/><path d="M5 6l1-3h8l1 3"/></svg>'

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    if '🚗' not in html:
        continue
    
    html = html.replace('<h1>🚗 ', f'<h1>{CAR_SVG} ')
    html = html.replace('🚗 ', '')  # Remove any remaining
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Fixed car emoji on {count} pages")
