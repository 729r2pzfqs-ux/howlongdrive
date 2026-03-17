import os
import re

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}') or '-to-' not in d:
        continue
    
    path = f'route/{d}/index.html'
    parts = d.split('-to-')
    if len(parts) != 2:
        continue
    
    from_city = parts[0].replace('-', ' ').title()
    to_city = parts[1].replace('-', ' ').title()
    
    with open(path) as f:
        html = f.read()
    
    # Skip if already has Google Maps link
    if 'google.com/maps' in html:
        continue
    
    # Add Google Maps link before the reverse or EV link
    maps_link = f'<a href="https://www.google.com/maps/dir/{from_city}/{to_city}" target="_blank" class="cta">📍 Open in Google Maps</a>\n            '
    
    # Find where to insert - before other cta buttons
    if 'class="cta"' in html:
        # Insert before first CTA
        html = re.sub(
            r'(<a href="[^"]*" class="cta">)',
            maps_link + r'\1',
            html,
            count=1
        )
    elif '</div>\s*</div>\s*<div id="map"' in html:
        # Insert before map
        html = re.sub(
            r'(</div>\s*</div>\s*<div id="map")',
            '</div>\n            ' + maps_link + r'\1',
            html
        )
    else:
        continue
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added Google Maps link to {count} pages")
