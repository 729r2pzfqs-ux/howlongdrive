import os

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find pages with the pattern: Google Maps link followed by Reverse and EV links inside hero
    if 'Open in Google Maps</a>' not in html:
        continue
    
    # Check if these buttons are inside hero section (problem case)
    if '.hero .cta' in html:
        continue  # Already has fix
    
    # Add CSS to make hero buttons display in a row
    if '.hero a.cta' not in html:
        css = '''
        .hero a.cta, .hero a.ev-link { display: inline-flex; align-items: center; gap: 0.5rem; margin-right: 0.75rem; margin-top: 1rem; }'''
        html = html.replace('</style>', css + '\n    </style>')
        
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Fixed button CSS on {count} pages")
