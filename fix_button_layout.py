import os
import re

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Skip if already has button-row
    if 'button-row' in html or 'btn-row' in html:
        continue
    
    # Only fix pages that have the Google Maps button inline with other buttons
    if 'Open in Google Maps</a>\n            <a href="/route/' not in html:
        continue
    
    # Wrap the three buttons in a div
    pattern = r'(<a href="https://www\.google\.com/maps/[^"]+[^<]+</a>\s*<a href="/route/[^"]+[^<]+</a>\s*<a href="/ev/[^"]+[^<]+</a>)'
    
    def wrap_buttons(match):
        return f'<div class="button-row">{match.group(1)}</div>'
    
    new_html = re.sub(pattern, wrap_buttons, html, flags=re.DOTALL)
    
    if new_html != html:
        # Add CSS for button-row if not present
        if '.button-row' not in new_html:
            css = '''
        .button-row { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1rem; }'''
            new_html = new_html.replace('</style>', css + '\n    </style>')
        
        with open(path, 'w') as f:
            f.write(new_html)
        count += 1

print(f"✅ Fixed button layout on {count} pages")
