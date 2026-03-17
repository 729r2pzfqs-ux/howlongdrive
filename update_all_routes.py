import os
import re

count = 0

for root, dirs, files in os.walk('route'):
    for f in files:
        if f != 'index.html':
            continue
        path = os.path.join(root, f)
        
        with open(path) as file:
            html = file.read()
        
        modified = False
        
        # Zoom out by 1 level (decrease zoom number)
        # Match patterns like .setView([lat, lon], 7) or .setView([lat,lon],8)
        zoom_match = re.search(r'\.setView\(\[([^]]+)\],\s*(\d+)\)', html)
        if zoom_match:
            old_zoom = int(zoom_match.group(2))
            new_zoom = max(3, old_zoom - 1)  # Don't go below 3
            html = re.sub(
                r'(\.setView\(\[[^]]+\],\s*)(\d+)(\))',
                lambda m: f'{m.group(1)}{new_zoom}{m.group(3)}',
                html
            )
            modified = True
        
        if modified:
            with open(path, 'w') as file:
                file.write(html)
            count += 1

print(f"✅ Updated zoom on {count} route pages")
