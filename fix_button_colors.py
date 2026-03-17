import os

count = 0

# New CSS for buttons
NEW_CSS = '''
        .hero .cta, .hero .ev-link { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.25rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; margin-right: 0.5rem; margin-top: 1rem; }
        .hero .cta { background: var(--primary); color: white; }
        .hero .cta:first-of-type { background: #EFA24F; }
        .hero .ev-link { background: var(--green); color: white; }'''

# Actually need specific classes - let me use a different approach
# Maps = orange, Reverse = blue, EV = green

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Skip if already fixed
    if 'maps-btn' in html:
        continue
    
    # Add specific classes to buttons
    html = html.replace(
        'class="cta">📍 Open in Google Maps</a>',
        'class="cta maps-btn">📍 Open in Google Maps</a>'
    )
    
    html = html.replace(
        'class="cta"><svg',
        'class="cta reverse-btn"><svg'
    )
    
    # Update CSS
    old_css = '.hero a.cta, .hero a.ev-link { display: inline-flex; align-items: center; gap: 0.5rem; margin-right: 0.75rem; margin-top: 1rem; }'
    new_css = '''.hero a.cta, .hero a.ev-link { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1.25rem; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; margin-right: 0.5rem; margin-top: 1rem; vertical-align: middle; }
        .hero .maps-btn { background: #EFA24F; color: white; }
        .hero .reverse-btn { background: var(--primary); color: white; }
        .hero .ev-link { background: var(--green); color: white; }'''
    
    html = html.replace(old_css, new_css)
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Fixed button colors on {count} pages")
