import os
import re

fixed = 0

for city in os.listdir('cities'):
    if not os.path.isdir(f'cities/{city}'):
        continue
    
    path = f'cities/{city}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find all route hrefs
    hrefs = re.findall(r'<a href="(/route/[^"]+/)" class="route-card">', html)
    
    # Check for duplicates
    seen = set()
    dups = []
    for href in hrefs:
        if href in seen:
            dups.append(href)
        else:
            seen.add(href)
    
    if not dups:
        continue
    
    # Remove duplicate entries
    for dup_href in set(dups):
        # Find all occurrences and keep only first
        pattern = rf'(<a href="{re.escape(dup_href)}" class="route-card">.*?</a>)\s*'
        matches = list(re.finditer(pattern, html, re.DOTALL))
        
        if len(matches) > 1:
            # Remove all but first occurrence (from end to preserve positions)
            for match in reversed(matches[1:]):
                html = html[:match.start()] + html[match.end():]
    
    # Update destination count
    remaining = len(re.findall(r'<a href="/route/[^"]+" class="route-card">', html))
    html = re.sub(
        r'<div class="stat-value">\d+</div><div class="stat-label">Destinations?</div>',
        f'<div class="stat-value">{remaining}</div><div class="stat-label">{"Destination" if remaining == 1 else "Destinations"}</div>',
        html
    )
    
    with open(path, 'w') as f:
        f.write(html)
    fixed += 1

print(f"✅ Fixed {fixed} city pages")
