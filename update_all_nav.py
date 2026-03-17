import os
import re

standard_nav = '<nav id="nav"><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/guides/">Guides</a><a href="/ev/" class="ev-badge">⚡ EV Trips</a><a href="/about/">About</a></nav>'

count = 0

# Update route pages
for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Replace nav (various patterns)
    old_html = html
    html = re.sub(r'<nav id="nav">.*?</nav>', standard_nav, html, flags=re.DOTALL)
    html = re.sub(r'<nav>.*?</nav>', standard_nav, html, flags=re.DOTALL)
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

# Update EV pages
for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    old_html = html
    html = re.sub(r'<nav id="nav">.*?</nav>', standard_nav, html, flags=re.DOTALL)
    html = re.sub(r'<nav>.*?</nav>', standard_nav, html, flags=re.DOTALL)
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

# Update city pages
for d in os.listdir('cities'):
    if not os.path.isdir(f'cities/{d}'):
        continue
    path = f'cities/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    old_html = html
    html = re.sub(r'<nav id="nav">.*?</nav>', standard_nav, html, flags=re.DOTALL)
    html = re.sub(r'<nav>.*?</nav>', standard_nav, html, flags=re.DOTALL)
    
    if html != old_html:
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Updated nav on {count} pages")
