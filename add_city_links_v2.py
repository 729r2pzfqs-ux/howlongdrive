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
    
    if from_city not in existing_cities or to_city not in existing_cities:
        continue
    
    with open(path) as f:
        html = f.read()
    
    if 'Explore Cities' in html:
        continue
    
    from_title = from_city.replace('-', ' ').title()
    to_title = to_city.replace('-', ' ').title()
    
    related_html = f'''
    <div class="related-section">
        <h3>Explore Cities</h3>
        <div class="related-links">
            <a href="/cities/{from_city}/">All routes from {from_title}</a>
            <a href="/cities/{to_city}/">All routes from {to_title}</a>
        </div>
    </div>
'''
    
    css = '''
        .related-section { background: #fff; padding: 1.5rem; border-radius: 1rem; margin: 1.5rem 0; max-width: 900px; margin-left: auto; margin-right: auto; }
        .related-section h3 { margin-bottom: 1rem; font-size: 1rem; color: #1e293b; }
        .related-links { display: flex; flex-wrap: wrap; gap: 0.75rem; }
        .related-links a { background: #f8fafc; padding: 0.5rem 1rem; border-radius: 0.5rem; text-decoration: none; color: #4B6E93; font-size: 0.875rem; }
        .related-links a:hover { background: #e2e8f0; }'''
    
    # Try </main> first, then try before </body>
    if '</main>' in html:
        html = html.replace('</main>', related_html + '</main>')
    elif '</body>' in html:
        # Insert before footer or </body>
        if '<footer' in html:
            html = re.sub(r'(\s*<footer)', related_html + r'\1', html)
        else:
            html = html.replace('</body>', related_html + '</body>')
    else:
        continue
    
    # Add CSS if not present
    if '.related-section' not in html:
        html = html.replace('</style>', css + '\n    </style>')
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added city links to {count} more route pages")
