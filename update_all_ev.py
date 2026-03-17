import os
import re

count = 0

for root, dirs, files in os.walk('ev'):
    for f in files:
        if f != 'index.html':
            continue
        path = os.path.join(root, f)
        
        with open(path) as file:
            html = file.read()
        
        zoom_match = re.search(r'\.setView\(\[([^]]+)\],\s*(\d+)\)', html)
        if zoom_match:
            old_zoom = int(zoom_match.group(2))
            new_zoom = max(3, old_zoom - 1)
            html = re.sub(
                r'(\.setView\(\[[^]]+\],\s*)(\d+)(\))',
                lambda m: f'{m.group(1)}{new_zoom}{m.group(3)}',
                html
            )
            with open(path, 'w') as file:
                file.write(html)
            count += 1

print(f"✅ Updated zoom on {count} EV pages")
