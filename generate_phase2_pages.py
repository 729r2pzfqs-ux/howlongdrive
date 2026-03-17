import os
import json

with open("data/phase2_routes.json") as f:
    routes = json.load(f)

# Read existing template from a working route
with open("route/new-york-to-los-angeles/index.html") as f:
    template_content = f.read()

# Count existing and new
count_route = 0
count_ev = 0

for r in routes:
    slug = f"{r['from_slug']}-to-{r['to_slug']}"
    
    # Skip if exists
    if os.path.exists(f"route/{slug}/index.html"):
        continue
    
    gas_cost = int(r['miles'] / 30 * 3.50)
    gallons = int(r['miles'] / 30)
    stops = max(0, (r['hours'] - 2) // 2)
    mid_lat = (r['from_lat'] + r['to_lat']) / 2
    mid_lon = (r['from_lon'] + r['to_lon']) / 2
    
    if r['miles'] > 1000: zoom = 5
    elif r['miles'] > 500: zoom = 6
    elif r['miles'] > 200: zoom = 7
    else: zoom = 8
    
    # Generate route page HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How Long to Drive from {r['from_name']} to {r['to_name']}? {r['hours']}h {r['mins']}min, {r['miles']} Miles</title>
    <meta name="description" content="How long to drive from {r['from_name']} to {r['to_name']}? {r['hours']}h {r['mins']}min driving time, {r['miles']} miles. Get gas costs, best times to drive, and route details.">
    <link rel="canonical" href="https://howlongdrive.com/route/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#4B6E93">
    <meta property="og:title" content="{r['from_name']} to {r['to_name']} - {r['hours']}h {r['mins']}min Drive Time">
    <meta property="og:description" content="Driving time from {r['from_name']} to {r['to_name']}: {r['hours']}h {r['mins']}min, {r['miles']} miles">
    <meta property="og:image" content="https://howlongdrive.com/assets/og-image.png">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How long does it take to drive from {r['from_name']} to {r['to_name']}?","acceptedAnswer":{{"@type":"Answer","text":"The drive from {r['from_name']} to {r['to_name']} takes approximately {r['hours']}h {r['mins']}min covering {r['miles']} miles."}}}},{{"@type":"Question","name":"How much does gas cost for {r['from_name']} to {r['to_name']}?","acceptedAnswer":{{"@type":"Answer","text":"At 30 MPG and $3.50/gallon, expect to spend approximately ${gas_cost} on gas for this {r['miles']}-mile trip."}}}}]}}</script>
    <style>
        :root {{ --primary: #4B6E93; --primary-dark: #3a5775; --accent: #EFA24F; --green: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 700; font-size: 1.5rem; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.75rem; }}
        .logo img {{ height: 180px; width: auto; }}
        nav {{ display: flex; align-items: center; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        nav a:hover {{ color: var(--primary); }}
        .ev-badge {{ background: var(--green); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }}
        .hamburger {{ display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; }}
        @media (max-width: 768px) {{
            .logo img {{ height: 144px; }} .logo span {{ display: none; }}
            nav {{ position: fixed; top: 0; right: -100%; width: 250px; height: 100vh; background: var(--card); flex-direction: column; padding: 5rem 2rem; transition: right 0.3s; z-index: 1000; }}
            nav.active {{ right: 0; }}
            nav a {{ font-size: 1.1rem; padding: 0.25rem 0; border-bottom: 1px solid var(--border); width: 100%; }}
            .hamburger {{ display: block; z-index: 1001; }}
            .close-btn {{ display: block; position: absolute; top: 1rem; right: 1rem; background: none; border: none; cursor: pointer; padding: 0.5rem; }}
            .overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; }}
            .overlay.active {{ display: block; }}
            .stats {{ grid-template-columns: 1fr 1fr !important; }}
            .grid {{ grid-template-columns: 1fr !important; }}
        }}
        .breadcrumb {{ font-size: 0.875rem; color: var(--muted); padding: 1rem 0; }}
        .breadcrumb a {{ color: var(--primary); text-decoration: none; }}
        .hero {{ background: linear-gradient(135deg, #4B6E93 0%, #3a5775 100%); padding: 2rem; border-radius: 1rem; margin-bottom: 1.5rem; color: white; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }}
        .subtitle {{ opacity: 0.9; margin-bottom: 1.5rem; font-size: 0.9rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }}
        .stat {{ text-align: center; padding: 1rem 0.5rem; background: rgba(255,255,255,0.15); border-radius: 0.5rem; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.9; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; }}
        .card {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card h3 {{ margin-bottom: 1rem; font-size: 0.9rem; color: var(--text); font-weight: 600; }}
        .row {{ display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--border); font-size: 0.875rem; }}
        .row:last-child {{ border: none; }}
        .row span:first-child {{ color: var(--muted); }}
        .row span:last-child {{ font-weight: 500; }}
        #map {{ height: 300px; border-radius: 0.75rem; margin-top: 1.5rem; }}
        .cta {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-top: 1.25rem; padding: 0.6rem 1.25rem; background: var(--accent); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        .ev-link {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-left: 0.75rem; padding: 0.6rem 1.25rem; background: var(--green); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        footer {{ text-align: center; padding: 2rem 1rem; color: var(--muted); font-size: 0.875rem; margin-top: 2rem; }}
        footer a {{ color: var(--primary); text-decoration: none; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G");</script></head>
<body>
    <header>
        <div class="container header-inner">
            <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
            <button class="hamburger" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
            <div class="overlay" onclick="toggleMenu()"></div>
            <nav id="nav">
                <button class="close-btn" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M18 6L6 18M6 6l12 12"/></svg></button>
                <a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/guides/">Guides</a><a href="/ev/" class="ev-badge">⚡ EV Routes</a>
            </nav>
        </div>
    </header>
    <main class="container">
        <div class="breadcrumb"><a href="/">Home</a> → <a href="/routes/">Routes</a> → {r['from_name']} to {r['to_name']}</div>
        <div class="hero">
            <h1>🚗 {r['from_name']} to {r['to_name']}</h1>
            <p class="subtitle">Regional driving route</p>
            <div class="stats">
                <div class="stat"><div class="stat-value">{r['hours']}h {r['mins']}m</div><div class="stat-label">Drive Time</div></div>
                <div class="stat"><div class="stat-value">{r['miles']}</div><div class="stat-label">Miles</div></div>
                <div class="stat"><div class="stat-value">${gas_cost}</div><div class="stat-label">Gas Cost</div></div>
                <div class="stat"><div class="stat-value">{stops}</div><div class="stat-label">Stops</div></div>
            </div>
        </div>
        <div class="grid">
            <div class="card">
                <h3>🗺️ Route Details</h3>
                <div class="row"><span>Distance</span><span>{r['miles']} miles</span></div>
                <div class="row"><span>Drive Time</span><span>{r['hours']}h {r['mins']}min</span></div>
                <div class="row"><span>Avg Speed</span><span>55 mph</span></div>
            </div>
            <div class="card">
                <h3>💰 Cost Breakdown</h3>
                <div class="row"><span>Gas (30 MPG)</span><span>${gas_cost}</span></div>
                <div class="row"><span>Tolls (est.)</span><span>$0-20</span></div>
                <div class="row"><span>Total</span><span>${gas_cost + 15}-${gas_cost + 50}</span></div>
            </div>
        </div>
        <div id="map"></div>
        <a href="https://www.google.com/maps/dir/{r['from_name']}/{r['to_name']}" target="_blank" class="cta">📍 Open in Google Maps</a>
        <a href="/ev/{slug}/" class="ev-link">⚡ View EV Route</a>
    </main>
    <footer><p>© 2026 HowLongDrive | <a href="/about/">About</a></p></footer>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        function toggleMenu() {{ document.getElementById('nav').classList.toggle('active'); document.querySelector('.overlay').classList.toggle('active'); }}
        const map = L.map('map').setView([{mid_lat}, {mid_lon}], {zoom});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{attribution: '© OpenStreetMap'}}).addTo(map);
        L.marker([{r['from_lat']}, {r['from_lon']}]).addTo(map).bindPopup('{r['from_name']}');
        L.marker([{r['to_lat']}, {r['to_lon']}]).addTo(map).bindPopup('{r['to_name']}');
        L.polyline([[{r['from_lat']}, {r['from_lon']}], [{r['to_lat']}, {r['to_lon']}]], {{color: '#4B6E93', weight: 3}}).addTo(map);
    </script>
</body>
</html>'''
    
    os.makedirs(f"route/{slug}", exist_ok=True)
    with open(f"route/{slug}/index.html", "w") as f:
        f.write(html)
    count_route += 1
    
    # Generate EV page
    charges = max(0, (r['miles'] - 250) // 250)
    charge_time = charges * 30
    total_hours = r['hours'] + (charge_time // 60)
    total_mins = r['mins'] + (charge_time % 60)
    if total_mins >= 60:
        total_hours += 1
        total_mins -= 60
    charge_cost = int(r['miles'] * 0.04)
    
    ev_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EV Drive: {r['from_name']} to {r['to_name']} | {total_hours}h {total_mins}min, {charges} Charging Stops</title>
    <meta name="description" content="Electric vehicle route from {r['from_name']} to {r['to_name']}. {total_hours}h {total_mins}min drive time, {r['miles']} miles, {charges} charging stops needed.">
    <link rel="canonical" href="https://howlongdrive.com/ev/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#10B981">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <style>
        :root {{ --primary: #10B981; --primary-dark: #059669; --accent: #EFA24F; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 700; font-size: 1.5rem; color: #4B6E93; text-decoration: none; display: flex; align-items: center; gap: 0.75rem; }}
        .logo img {{ height: 180px; width: auto; }}
        nav {{ display: flex; align-items: center; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--primary); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }}
        .hamburger {{ display: none; }}
        @media (max-width: 768px) {{
            .logo img {{ height: 144px; }}
            nav {{ position: fixed; top: 0; right: -100%; width: 250px; height: 100vh; background: var(--card); flex-direction: column; padding: 5rem 2rem; transition: right 0.3s; z-index: 1000; }}
            nav.active {{ right: 0; }}
            .hamburger {{ display: block; z-index: 1001; background: none; border: none; cursor: pointer; padding: 0.5rem; }}
            .stats {{ grid-template-columns: 1fr 1fr !important; }}
            .grid {{ grid-template-columns: 1fr !important; }}
        }}
        .breadcrumb {{ font-size: 0.875rem; color: var(--muted); padding: 1rem 0; }}
        .breadcrumb a {{ color: var(--primary); text-decoration: none; }}
        .hero {{ background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 2rem; border-radius: 1rem; margin-bottom: 1.5rem; color: white; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; font-weight: 600; }}
        .subtitle {{ opacity: 0.9; margin-bottom: 1.5rem; font-size: 0.9rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }}
        .stat {{ text-align: center; padding: 1rem 0.5rem; background: rgba(255,255,255,0.15); border-radius: 0.5rem; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.9; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; }}
        .card {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card h3 {{ margin-bottom: 1rem; font-size: 0.9rem; }}
        .row {{ display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--border); font-size: 0.875rem; }}
        .row:last-child {{ border: none; }}
        .row span:first-child {{ color: var(--muted); }}
        #map {{ height: 300px; border-radius: 0.75rem; margin-top: 1.5rem; }}
        .cta {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-top: 1.25rem; padding: 0.6rem 1.25rem; background: var(--accent); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        .gas-link {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-left: 0.75rem; padding: 0.6rem 1.25rem; background: #4B6E93; color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        footer {{ text-align: center; padding: 2rem 1rem; color: var(--muted); font-size: 0.875rem; margin-top: 2rem; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G");</script></head>
<body>
    <header>
        <div class="container header-inner">
            <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
            <button class="hamburger" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
            <div class="overlay" onclick="toggleMenu()"></div>
            <nav id="nav">
                <a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/ev/" class="ev-badge">⚡ EV Routes</a>
            </nav>
        </div>
    </header>
    <main class="container">
        <div class="breadcrumb"><a href="/">Home</a> → <a href="/ev/">EV Routes</a> → {r['from_name']} to {r['to_name']}</div>
        <div class="hero">
            <h1>⚡ EV: {r['from_name']} to {r['to_name']}</h1>
            <p class="subtitle">Electric vehicle route with charging stops</p>
            <div class="stats">
                <div class="stat"><div class="stat-value">{total_hours}h {total_mins}m</div><div class="stat-label">Total Time</div></div>
                <div class="stat"><div class="stat-value">{r['miles']}</div><div class="stat-label">Miles</div></div>
                <div class="stat"><div class="stat-value">{charges}</div><div class="stat-label">Charges</div></div>
                <div class="stat"><div class="stat-value">${charge_cost}</div><div class="stat-label">Est. Cost</div></div>
            </div>
        </div>
        <div class="grid">
            <div class="card">
                <h3>⚡ EV Details</h3>
                <div class="row"><span>Distance</span><span>{r['miles']} miles</span></div>
                <div class="row"><span>Drive Time</span><span>{r['hours']}h {r['mins']}min</span></div>
                <div class="row"><span>Charging Stops</span><span>{charges}</span></div>
            </div>
            <div class="card">
                <h3>💰 Cost Comparison</h3>
                <div class="row"><span>EV Charging</span><span>${charge_cost}</span></div>
                <div class="row"><span>Gas Car</span><span>${gas_cost}</span></div>
                <div class="row"><span>Savings</span><span style="color:#10B981">${gas_cost - charge_cost}</span></div>
            </div>
        </div>
        <div id="map"></div>
        <a href="https://www.google.com/maps/dir/{r['from_name']}/{r['to_name']}" target="_blank" class="cta">📍 Google Maps</a>
        <a href="/route/{slug}/" class="gas-link">⛽ Gas Route</a>
    </main>
    <footer><p>© 2026 HowLongDrive</p></footer>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        function toggleMenu() {{ document.getElementById('nav').classList.toggle('active'); }}
        const map = L.map('map').setView([{mid_lat}, {mid_lon}], {zoom});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{attribution: '© OpenStreetMap'}}).addTo(map);
        L.marker([{r['from_lat']}, {r['from_lon']}]).addTo(map);
        L.marker([{r['to_lat']}, {r['to_lon']}]).addTo(map);
        L.polyline([[{r['from_lat']}, {r['from_lon']}], [{r['to_lat']}, {r['to_lon']}]], {{color: '#10B981', weight: 3}}).addTo(map);
    </script>
</body>
</html>'''
    
    os.makedirs(f"ev/{slug}", exist_ok=True)
    with open(f"ev/{slug}/index.html", "w") as f:
        f.write(ev_html)
    count_ev += 1

print(f"✅ Generated {count_route} new route pages")
print(f"✅ Generated {count_ev} new EV pages")
