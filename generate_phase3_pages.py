import os
import json

with open("data/phase3_routes.json") as f:
    routes = json.load(f)

count_route = 0
count_ev = 0

for r in routes:
    slug = f"{r['from_slug']}-to-{r['to_slug']}"
    
    if os.path.exists(f"route/{slug}/index.html"):
        continue
    
    gas_cost = int(r['miles'] / 30 * 3.50)
    stops = max(0, (r['hours'] - 2) // 2)
    mid_lat = (r['from_lat'] + r['to_lat']) / 2
    mid_lon = (r['from_lon'] + r['to_lon']) / 2
    
    if r['miles'] > 2000: zoom = 4
    elif r['miles'] > 1000: zoom = 5
    elif r['miles'] > 500: zoom = 6
    else: zoom = 7
    
    # Route page
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How Long to Drive from {r['from_name']} to {r['to_name']}? {r['hours']}h {r['mins']}min</title>
    <meta name="description" content="Drive from {r['from_name']} to {r['to_name']}: {r['hours']}h {r['mins']}min, {r['miles']} miles. Gas cost, route details.">
    <link rel="canonical" href="https://howlongdrive.com/route/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#4B6E93">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <style>
        :root {{ --primary: #4B6E93; --green: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ color: var(--primary); text-decoration: none; display: flex; align-items: center; }}
        .logo img {{ height: 180px; }}
        nav {{ display: flex; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--green); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; }}
        .hamburger {{ display: none; background: none; border: none; cursor: pointer; }}
        @media (max-width: 768px) {{
            .logo img {{ height: 144px; }}
            nav {{ position: fixed; top: 0; right: -100%; width: 250px; height: 100vh; background: var(--card); flex-direction: column; padding: 5rem 2rem; transition: right 0.3s; z-index: 1000; }}
            nav.active {{ right: 0; }}
            .hamburger {{ display: block; z-index: 1001; }}
            .stats {{ grid-template-columns: 1fr 1fr !important; }}
            .grid {{ grid-template-columns: 1fr !important; }}
        }}
        .hero {{ background: linear-gradient(135deg, #4B6E93, #3a5775); padding: 2rem; border-radius: 1rem; margin: 1rem 0; color: white; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-top: 1rem; }}
        .stat {{ text-align: center; padding: 1rem; background: rgba(255,255,255,0.15); border-radius: 0.5rem; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.9; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; }}
        .card {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card h3 {{ margin-bottom: 1rem; font-size: 0.9rem; }}
        .row {{ display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--border); font-size: 0.875rem; }}
        .row:last-child {{ border: none; }}
        #map {{ height: 300px; border-radius: 0.75rem; margin-top: 1rem; }}
        .cta {{ display: inline-block; margin-top: 1rem; padding: 0.6rem 1.25rem; background: #EFA24F; color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        .ev-link {{ margin-left: 0.75rem; background: var(--green); }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G");</script></head>
<body>
    <header><div class="container header-inner">
        <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
        <button class="hamburger" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
        <nav id="nav"><a href="/">Home</a><a href="/routes/">Routes</a><a href="/ev/" class="ev-badge">⚡ EV</a></nav>
    </div></header>
    <main class="container">
        <div class="hero">
            <h1>🚗 {r['from_name']} to {r['to_name']}</h1>
            <div class="stats">
                <div class="stat"><div class="stat-value">{r['hours']}h {r['mins']}m</div><div class="stat-label">Drive Time</div></div>
                <div class="stat"><div class="stat-value">{r['miles']}</div><div class="stat-label">Miles</div></div>
                <div class="stat"><div class="stat-value">${gas_cost}</div><div class="stat-label">Gas Cost</div></div>
                <div class="stat"><div class="stat-value">{stops}</div><div class="stat-label">Stops</div></div>
            </div>
        </div>
        <div class="grid">
            <div class="card"><h3>🗺️ Route Details</h3>
                <div class="row"><span>Distance</span><span>{r['miles']} mi</span></div>
                <div class="row"><span>Drive Time</span><span>{r['hours']}h {r['mins']}min</span></div>
                <div class="row"><span>Avg Speed</span><span>55 mph</span></div>
            </div>
            <div class="card"><h3>💰 Cost</h3>
                <div class="row"><span>Gas (30 MPG)</span><span>${gas_cost}</span></div>
                <div class="row"><span>Tolls (est.)</span><span>$0-20</span></div>
                <div class="row"><span>Total</span><span>${gas_cost + 15}-${gas_cost + 50}</span></div>
            </div>
        </div>
        <div id="map"></div>
        <a href="https://www.google.com/maps/dir/{r['from_name']}/{r['to_name']}" target="_blank" class="cta">📍 Google Maps</a>
        <a href="/ev/{slug}/" class="cta ev-link">⚡ EV Route</a>
    </main>
    <footer>© 2026 HowLongDrive</footer>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        function toggleMenu(){{document.getElementById('nav').classList.toggle('active');}}
        const map=L.map('map').setView([{mid_lat},{mid_lon}],{zoom});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OSM'}}).addTo(map);
        L.marker([{r['from_lat']},{r['from_lon']}]).addTo(map);
        L.marker([{r['to_lat']},{r['to_lon']}]).addTo(map);
        L.polyline([[{r['from_lat']},{r['from_lon']}],[{r['to_lat']},{r['to_lon']}]],{{color:'#4B6E93',weight:3}}).addTo(map);
    </script>
</body>
</html>'''
    
    os.makedirs(f"route/{slug}", exist_ok=True)
    with open(f"route/{slug}/index.html", "w") as f:
        f.write(html)
    count_route += 1
    
    # EV page
    charges = max(0, (r['miles'] - 250) // 250)
    charge_cost = int(r['miles'] * 0.04)
    
    ev_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EV: {r['from_name']} to {r['to_name']} | {charges} Charging Stops</title>
    <meta name="description" content="EV route {r['from_name']} to {r['to_name']}: {r['miles']} miles, {charges} charging stops.">
    <link rel="canonical" href="https://howlongdrive.com/ev/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#10B981">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <style>
        :root {{ --primary: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ color: #4B6E93; text-decoration: none; }}
        .logo img {{ height: 180px; }}
        nav {{ display: flex; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--primary); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; }}
        .hamburger {{ display: none; }}
        @media (max-width: 768px) {{ .logo img {{ height: 144px; }} nav {{ display: none; }} .hamburger {{ display: block; }} .stats {{ grid-template-columns: 1fr 1fr !important; }} .grid {{ grid-template-columns: 1fr !important; }} }}
        .hero {{ background: linear-gradient(135deg, #10B981, #059669); padding: 2rem; border-radius: 1rem; margin: 1rem 0; color: white; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-top: 1rem; }}
        .stat {{ text-align: center; padding: 1rem; background: rgba(255,255,255,0.15); border-radius: 0.5rem; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.9; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem; }}
        .card {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card h3 {{ margin-bottom: 1rem; font-size: 0.9rem; }}
        .row {{ display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--border); font-size: 0.875rem; }}
        .row:last-child {{ border: none; }}
        #map {{ height: 300px; border-radius: 0.75rem; margin-top: 1rem; }}
        .cta {{ display: inline-block; margin-top: 1rem; padding: 0.6rem 1.25rem; background: #EFA24F; color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        .gas-link {{ margin-left: 0.75rem; background: #4B6E93; }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G");</script></head>
<body>
    <header><div class="container header-inner">
        <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
        <nav><a href="/">Home</a><a href="/ev/" class="ev-badge">⚡ EV</a></nav>
    </div></header>
    <main class="container">
        <div class="hero">
            <h1>⚡ EV: {r['from_name']} to {r['to_name']}</h1>
            <div class="stats">
                <div class="stat"><div class="stat-value">{r['hours']}h+</div><div class="stat-label">Total Time</div></div>
                <div class="stat"><div class="stat-value">{r['miles']}</div><div class="stat-label">Miles</div></div>
                <div class="stat"><div class="stat-value">{charges}</div><div class="stat-label">Charges</div></div>
                <div class="stat"><div class="stat-value">${charge_cost}</div><div class="stat-label">Cost</div></div>
            </div>
        </div>
        <div class="grid">
            <div class="card"><h3>⚡ EV Details</h3>
                <div class="row"><span>Distance</span><span>{r['miles']} mi</span></div>
                <div class="row"><span>Charging Stops</span><span>{charges}</span></div>
            </div>
            <div class="card"><h3>💰 Savings</h3>
                <div class="row"><span>EV Cost</span><span>${charge_cost}</span></div>
                <div class="row"><span>Gas Cost</span><span>${gas_cost}</span></div>
                <div class="row"><span>Savings</span><span style="color:#10B981">${gas_cost - charge_cost}</span></div>
            </div>
        </div>
        <div id="map"></div>
        <a href="https://www.google.com/maps/dir/{r['from_name']}/{r['to_name']}" class="cta">📍 Maps</a>
        <a href="/route/{slug}/" class="cta gas-link">⛽ Gas</a>
    </main>
    <footer>© 2026 HowLongDrive</footer>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const map=L.map('map').setView([{mid_lat},{mid_lon}],{zoom});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{attribution:'© OSM'}}).addTo(map);
        L.marker([{r['from_lat']},{r['from_lon']}]).addTo(map);
        L.marker([{r['to_lat']},{r['to_lon']}]).addTo(map);
        L.polyline([[{r['from_lat']},{r['from_lon']}],[{r['to_lat']},{r['to_lon']}]],{{color:'#10B981',weight:3}}).addTo(map);
    </script>
</body>
</html>'''
    
    os.makedirs(f"ev/{slug}", exist_ok=True)
    with open(f"ev/{slug}/index.html", "w") as f:
        f.write(ev_html)
    count_ev += 1

print(f"✅ Generated {count_route} route pages")
print(f"✅ Generated {count_ev} EV pages")
