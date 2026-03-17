import os
import re

existing_cities = set(os.listdir('cities'))
count = 0

for root, dirs, files in os.walk('route'):
    for f in files:
        if f != 'index.html':
            continue
        path = os.path.join(root, f)
        
        with open(path) as file:
            html = file.read()
        
        if 'related-section' not in html:
            continue
        
        # Find city links in this page
        city_links = re.findall(r'<a href="/cities/([^/]+)/">[^<]+</a>', html)
        
        # Check if all cities exist
        all_exist = all(city in existing_cities for city in city_links)
        
        if not all_exist:
            # Remove the entire related-section
            html = re.sub(r'\s*<div class="related-section">.*?</div></div></div>\s*', '\n    ', html, flags=re.DOTALL)
            with open(path, 'w') as file:
                file.write(html)
            count += 1

print(f"✅ Removed broken city links from {count} pages")
