import os
import json

with open("data/phase2_routes.json") as f:
    routes_data = json.load(f)

SVG_MAP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'
SVG_DOLLAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>'
SVG_FAQ = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3M12 17h.01"/></svg>'
SVG_CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'

count = 0
for r in routes_data:
    slug = f"{r['from_slug']}-to-{r['to_slug']}"
    
    for path in [f"route/{slug}/index.html", f"ev/{slug}/index.html"]:
        if not os.path.exists(path):
            continue
        
        with open(path) as f:
            html = f.read()
        
        modified = False
        
        # Replace emoji h3
        if '🗺️' in html or '💰' in html:
            html = html.replace('<h3>🗺️ Route Details</h3>', f'<h3>{SVG_MAP} Route Details</h3>')
            html = html.replace('<h3>💰 Cost Breakdown</h3>', f'<h3>{SVG_DOLLAR} Cost Breakdown</h3>')
            html = html.replace('<h3>💰 Cost</h3>', f'<h3>{SVG_DOLLAR} Cost Breakdown</h3>')
            html = html.replace('<h3>⚡ EV Details</h3>', f'<h3>{SVG_MAP} EV Details (300mi range)</h3>')
            modified = True
        
        # Fix button text
        if '>📍 Google Maps</a>' in html:
            html = html.replace('>📍 Google Maps</a>', '>📍 Open in Google Maps</a>')
            modified = True
        
        # Add FAQ if missing
        if 'class="faq"' not in html and 'route/' in path:
            faq_html = f'''
        <div class="faq">
            <h2>{SVG_FAQ} FAQ</h2>
            <div class="faq-item open"><div class="faq-q" onclick="this.parentElement.classList.toggle('open')">How long is the drive from {r['from_name']} to {r['to_name']}?{SVG_CHEVRON}</div><div class="faq-a">The drive takes approximately <strong>{r['hours']} hours and {r['mins']} minutes</strong> covering {r['miles']} miles.</div></div>
            <div class="faq-item"><div class="faq-q" onclick="this.parentElement.classList.toggle('open')">How much gas will I need?{SVG_CHEVRON}</div><div class="faq-a">At 30 MPG, you'll use about {r['miles']//30} gallons of gas, costing approximately ${int(r['miles']/30*3.5)} at $3.50/gallon.</div></div>
        </div>
'''
            html = html.replace('</main>', faq_html + '    </main>')
            modified = True
        
        if modified:
            with open(path, 'w') as f:
                f.write(html)
            count += 1

print(f"✅ Fixed {count} Phase 2 pages")
