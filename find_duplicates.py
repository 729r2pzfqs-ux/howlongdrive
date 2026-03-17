import os
import re
from collections import Counter

duplicates = []

for city in os.listdir('cities'):
    if not os.path.isdir(f'cities/{city}'):
        continue
    
    path = f'cities/{city}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find all route hrefs
    hrefs = re.findall(r'href="(/route/[^"]+/)"', html)
    
    # Count occurrences
    counts = Counter(hrefs)
    
    # Check for duplicates
    dups = [(href, count) for href, count in counts.items() if count > 1]
    
    if dups:
        duplicates.append((city, dups))

print(f"Found {len(duplicates)} city pages with duplicates:")
for city, dups in duplicates:
    for href, count in dups:
        print(f"  {city}: {href} appears {count}x")
