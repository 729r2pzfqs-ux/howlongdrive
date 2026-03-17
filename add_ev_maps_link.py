import os
import re

count = 0

for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    
    # Parse from-to from directory name
    if '-to-' not in d:
        continue
    
    parts = d.split('-to-')
    from_city = parts[0].replace('-', ' ').title()
    to_city = parts[1].replace('-', ' ').title()
    
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Skip if already has maps link
    if 'google.com/maps' in html:
        continue
    
    # Find the hero buttons section and add maps link
    # Look for the EV link or reverse link in hero
    maps_btn = f'''<a href="https://www.google.com/maps/dir/{from_city}/{to_city}" target="_blank" class="cta maps-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg> Open in Google Maps</a>'''
    
    # Add CSS for maps-btn if not present
    if '.maps-btn' not in html:
        html = html.replace('.hero .cta {', '.hero .maps-btn { background: #EFA24F; color: white; }\n        .hero .cta {')
    
    # Find the buttons div in hero and add maps link
    # Pattern: look for </a> followed by </div> in the hero buttons area
    if '<div class="buttons">' in html:
        # Add before </div> that closes buttons
        html = re.sub(
            r'(class="cta ev-link"[^>]*>[^<]*</a>)\s*(</div>\s*</div>\s*</section>)',
            r'\1\n            ' + maps_btn + r'\2',
            html
        )
    elif 'class="cta reverse-btn"' in html:
        # Add after reverse button
        html = re.sub(
            r'(class="cta reverse-btn"[^>]*>[^<]*</a>)',
            r'\1\n            ' + maps_btn,
            html
        )
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added Google Maps link to {count} EV pages")
