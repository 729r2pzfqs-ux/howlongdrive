#!/usr/bin/env python3
"""Fix all navbar inconsistencies across the site."""
import os
import re
import glob

CANONICAL_HEADER = '''<header>
        <div class="container header-inner">
            <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
            <button class="hamburger" onclick="toggleMenu()" aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
            <div class="overlay" onclick="toggleMenu()"></div>
            <nav id="nav"><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/guides/">Guides</a><a href="/ev/" class="ev-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> EV Trips</a><a href="/about/">About</a></nav>
        </div>
    </header>'''

HAMBURGER_CSS = """
.hamburger { display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; }
.hamburger svg { width: 24px; height: 24px; color: var(--text, #1e293b); }
.overlay { display: none; }
@media (max-width: 768px) {
    .logo img { height: 100px !important; }
    nav { position: fixed; top: 0; right: -100%; width: 250px; height: 100vh; background: var(--card, #fff); flex-direction: column; padding: 5rem 2rem; transition: right 0.3s; z-index: 1000; box-shadow: -2px 0 10px rgba(0,0,0,0.1); }
    nav.active { right: 0; display: flex; }
    nav a { font-size: 1.1rem; padding: 0.75rem 0; border-bottom: 1px solid var(--border, #e2e8f0); width: 100%; }
    .hamburger { display: block; z-index: 1001; }
    .overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; }
    .overlay.active { display: block; }
}
"""

TOGGLE_MENU_JS = """<script>
function toggleMenu() {
    document.getElementById('nav').classList.toggle('active');
    document.querySelector('.overlay').classList.toggle('active');
}
</script>"""

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # 1. Replace header HTML
    content = re.sub(r'<header>.*?</header>', CANONICAL_HEADER, content, count=1, flags=re.DOTALL)
    # Also handle <header><div... (no newline) variant
    content = re.sub(r'<header><div.*?</header>', CANONICAL_HEADER, content, count=1, flags=re.DOTALL)
    
    # 2. Remove .nav-links references from CSS (homepage uses this)
    # Replace .nav-links styles with nav styles if present
    content = content.replace('.nav-links.active', 'nav.active')
    content = content.replace('.nav-links a', 'nav a')
    content = content.replace('.nav-links {', 'nav.mobile-override {')  # deactivate old rule
    
    # 3. Add hamburger CSS if missing
    if '.hamburger' not in content.split('</header>')[0].split('<style>')[-1] if '<style>' in content else True:
        # Check if hamburger CSS is already in the stylesheet
        style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if style_match:
            css = style_match.group(1)
            if '.hamburger' not in css:
                # Add hamburger CSS before closing </style>
                content = content.replace('</style>', HAMBURGER_CSS + '</style>', 1)
    
    # 4. Add toggleMenu JS if missing
    if 'function toggleMenu' not in content:
        # Add before </body>
        content = content.replace('</body>', TOGGLE_MENU_JS + '</body>')
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
changed = 0
total = 0
errors = []

# Find all HTML files
html_files = []
for root, dirs, files in os.walk('.'):
    # Skip .git
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Found {len(html_files)} HTML files")

for filepath in html_files:
    total += 1
    try:
        if fix_file(filepath):
            changed += 1
    except Exception as e:
        errors.append((filepath, str(e)))

print(f"Changed: {changed}/{total}")
if errors:
    print(f"Errors: {len(errors)}")
    for path, err in errors[:5]:
        print(f"  {path}: {err}")
