import os
import re
from collections import Counter

fixed = 0

for city in os.listdir('cities'):
    if not os.path.isdir(f'cities/{city}'):
        continue
    
    path = f'cities/{city}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find all route cards
    route_pattern = r'<a href="(/route/[^"]+/)" class="route-card">\s*<div><div class="route-title">([^<]+)</div><div class="route-meta">[^<]+</div></div>\s*<div class="route-time">[^<]+</div>\s*</a>'
    
    routes = re.findall(route_pattern, html, re.DOTALL)
    
    if not routes:
        continue
    
    # Check for duplicates
    seen_hrefs = set()
    unique_routes = []
    duplicates_found = False
    
    for match in re.finditer(route_pattern, html, re.DOTALL):
        href = match.group(1)
        if href not in seen_hrefs:
            seen_hrefs.add(href)
            unique_routes.append(match.group(0))
        else:
            duplicates_found = True
    
    if not duplicates_found:
        continue
    
    # Rebuild routes section
    routes_start = re.search(r'<div class="routes">', html)
    routes_end = re.search(r'</div>\s*</div>\s*<footer>', html)
    
    if routes_start and routes_end:
        new_routes_html = '<div class="routes">\n            ' + '\n            '.join(unique_routes) + '</div>'
        html = html[:routes_start.start()] + new_routes_html + '\n        ' + html[routes_end.start()+6:]
        
        # Update destination count
        count = len(unique_routes)
        html = re.sub(r'<div class="stat-value">\d+</div><div class="stat-label">Destinations?</div>', 
                     f'<div class="stat-value">{count}</div><div class="stat-label">{"Destination" if count == 1 else "Destinations"}</div>', 
                     html)
        
        with open(path, 'w') as f:
            f.write(html)
        fixed += 1

print(f"✅ Fixed {fixed} city pages with duplicate routes")
