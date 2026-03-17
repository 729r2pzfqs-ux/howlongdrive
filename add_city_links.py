import os
import re

existing_cities = set(os.listdir('cities'))
count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}') or '-to-' not in d:
        continue
    
    path = f'route/{d}/index.html'
    parts = d.split('-to-')
    if len(parts) != 2:
        continue
    
    from_city = parts[0]
    to_city = parts[1]
    
    # Check if both cities exist
    if from_city not in existing_cities or to_city not in existing_cities:
        continue
    
    with open(path) as f:
        html = f.read()
    
    # Skip if already has city links
    if 'Explore Cities' in html:
        continue
    
    from_title = from_city.replace('-', ' ').title()
    to_title = to_city.replace('-', ' ').title()
    
    # Add related section before </main>
    related_html = f'''
        <div class="related-section">
            <h3>Explore Cities</h3>
            <div class="related-links">
                <a href="/cities/{from_city}/">All routes from {from_title}</a>
                <a href="/cities/{to_city}/">All routes from {to_title}</a>
            </div>
        </div>
'''
    
    html = html.replace('</main>', related_html + '    </main>')
    
    # Add CSS if not present
    if '.related-section' not in html:
        css = '''
        .related-section { background: var(--card); padding: 1.5rem; border-radius: 1rem; margin: 1.5rem 0; }
        .related-section h3 { margin-bottom: 1rem; font-size: 1rem; }
        .related-links { display: flex; flex-wrap: wrap; gap: 0.75rem; }
        .related-links a { background: var(--bg); padding: 0.5rem 1rem; border-radius: 0.5rem; text-decoration: none; color: var(--primary); font-size: 0.875rem; }
        .related-links a:hover { background: var(--border); }'''
        html = html.replace('</style>', css + '\n    </style>')
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added city links to {count} route pages")
