import os
import re

count = 0

for city in os.listdir('cities'):
    if not os.path.isdir(f'cities/{city}'):
        continue
    
    path = f'cities/{city}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find all route links
    # Keep only routes that start with this city (city-to-X)
    # Remove routes that end with this city (X-to-city)
    
    # Pattern for routes TO this city (should be removed)
    reverse_pattern = rf'<a href="/route/[^"]*-to-{re.escape(city)}/" class="route-card"[^>]*>.*?</a>\s*'
    
    # Count how many we're removing
    reverse_matches = re.findall(reverse_pattern, html, re.DOTALL)
    
    if len(reverse_matches) > 0:
        # Remove reverse routes
        html = re.sub(reverse_pattern, '', html, flags=re.DOTALL)
        
        # Update the route count
        remaining = len(re.findall(r'class="route-card"', html))
        if remaining == 1:
            html = re.sub(r'\d+ driving routes? available', '1 driving route available', html)
        else:
            html = re.sub(r'\d+ driving routes? available', f'{remaining} driving routes available', html)
        
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Fixed {count} city pages with duplicate routes")
