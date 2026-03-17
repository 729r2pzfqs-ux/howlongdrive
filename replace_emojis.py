import os

# SVG icons
MAP_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'
BOLT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>'

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    old_html = html
    
    # Replace emojis
    html = html.replace('📍 Open in Google Maps', f'{MAP_PIN} Open in Google Maps')
    html = html.replace('>⚡ EV', f'>{BOLT} EV')
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

# Also do EV pages
for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    old_html = html
    html = html.replace('📍 Open in Google Maps', f'{MAP_PIN} Open in Google Maps')
    html = html.replace('📍 Google Maps', f'{MAP_PIN} Google Maps')
    html = html.replace('>⚡ EV', f'>{BOLT} EV')
    html = html.replace('>⛽ Gas', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M3 22V6a2 2 0 012-2h8a2 2 0 012 2v16M7 10h4"/><path d="M15 22v-4a3 3 0 016 0v4"/><path d="M22 22V10l-3-8"/></svg> Gas')
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Replaced emojis on {count} pages")
