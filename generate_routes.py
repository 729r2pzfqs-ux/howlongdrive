import json
import os

# Load all routes
routes = []
for f in ['data/routes.json', 'data/routes_expanded.json']:
    if os.path.exists(f):
        with open(f, 'r') as file:
            routes.extend(json.load(file))

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{from_city} to {to_city} Driving Time - {time}, {miles} miles | HowLongDrive</title>
    <meta name="description" content="How long to drive from {from_city} to {to_city}? {time} driving time, {miles} miles via {highway}. Get gas costs, best times to drive, and route details.">
    <link rel="canonical" href="https://howlongdrive.com/route/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#4B6E93">
    <meta property="og:title" content="{from_city} to {to_city} - {time} Drive Time">
    <meta property="og:description" content="Driving time from {from_city} to {to_city}: {time}, {miles} miles via {highway}">
    <meta property="og:image" content="https://howlongdrive.com/assets/og-image.png">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"TravelAction","name":"{from_city} to {to_city}","fromLocation":{{"@type":"Place","name":"{from_city}"}},"toLocation":{{"@type":"Place","name":"{to_city}"}},"distance":{{"@type":"Distance","name":"{miles} miles"}}}}</script>
    <style>
        :root {{ --primary: #4B6E93; --primary-dark: #3a5775; --accent: #EFA24F; --accent-dark: #d88a3a; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.75rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 700; font-size: 1.5rem; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.75rem; }}
        .logo img {{ height: 50px; width: auto; }}
        nav a {{ color: var(--muted); text-decoration: none; margin-left: 1.5rem; font-size: 0.875rem; }}
        nav a:hover {{ color: var(--primary); }}
        .breadcrumb {{ font-size: 0.875rem; color: var(--muted); padding: 1rem 0; }}
        .breadcrumb a {{ color: var(--primary); text-decoration: none; }}
        .hero {{ background: var(--card); padding: 2rem; border-radius: 1rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 1.75rem; margin-bottom: 0.5rem; color: var(--primary); }}
        .subtitle {{ color: var(--muted); margin-bottom: 1.5rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }}
        .stat {{ text-align: center; padding: 1.5rem; background: var(--bg); border-radius: 0.75rem; }}
        .stat-value {{ font-size: 2rem; font-weight: 700; color: var(--primary); }}
        .stat-label {{ color: var(--muted); font-size: 0.875rem; margin-top: 0.25rem; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; }}
        @media (max-width: 640px) {{ .grid, .stats {{ grid-template-columns: 1fr; }} }}
        .card {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .card h3 {{ margin-bottom: 1rem; font-size: 1rem; color: var(--primary); }}
        .row {{ display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border); }}
        .row:last-child {{ border: none; }}
        .row a {{ color: var(--primary); text-decoration: none; }}
        .reverse-link {{ display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: var(--accent); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; }}
        .reverse-link:hover {{ background: var(--accent-dark); }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; margin-top: 2rem; }}
        footer a {{ color: var(--primary); text-decoration: none; }}
    </style>
</head>
<body>
    <header>
        <div class="container header-inner">
            <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"><span>HowLongDrive</span></a>
            <nav><a href="/">Home</a><a href="/routes/">Routes</a></nav>
        </div>
    </header>
    <div class="container">
        <div class="breadcrumb"><a href="/">Home</a> → <a href="/routes/">Routes</a> → {from_city} to {to_city}</div>
        <div class="hero">
            <h1>🚗 {from_city} to {to_city}</h1>
            <p class="subtitle">via {highway}</p>
            <div class="stats">
                <div class="stat"><div class="stat-value">{time}</div><div class="stat-label">⏱️ Drive Time</div></div>
                <div class="stat"><div class="stat-value">{miles}</div><div class="stat-label">📏 Miles</div></div>
                <div class="stat"><div class="stat-value">${gas_cost}</div><div class="stat-label">⛽ Est. Gas</div></div>
            </div>
            <a href="/route/{reverse_slug}/" class="reverse-link">🔄 {to_city} → {from_city}</a>
        </div>
        <div class="grid">
            <div class="card"><h3>🛣️ Route Details</h3><div class="row"><span>Distance</span><span>{miles} mi ({km} km)</span></div><div class="row"><span>Drive Time</span><span>{time}</span></div><div class="row"><span>Route</span><span>{highway}</span></div><div class="row"><span>Avg Speed</span><span>{avg_speed} mph</span></div></div>
            <div class="card"><h3>💰 Trip Cost</h3><div class="row"><span>Gas (~{gallons} gal)</span><span>${gas_cost}</span></div><div class="row"><span>Est. Tolls</span><span>${tolls}</span></div><div class="row"><span><strong>Total</strong></span><span><strong>${total_cost}</strong></span></div></div>
            <div class="card"><h3>⏰ Best Times to Drive</h3><div class="row"><span>Fastest</span><span>Weekdays 10am-3pm</span></div><div class="row"><span>Avoid</span><span>Fri 3-7pm, Sun 4-8pm</span></div><div class="row"><span>Rush Hour</span><span>+30min to +2hr</span></div></div>
            <div class="card"><h3>🔄 Return Trip</h3><div class="row"><a href="/route/{reverse_slug}/">{to_city} → {from_city}</a><span>{time}</span></div></div>
        </div>
    </div>
    <footer><p>© 2026 <a href="/">HowLongDrive.com</a></p></footer>
</body>
</html>'''

count = 0
processed = set()

for route in routes:
    from_city = route['from']
    to_city = route['to']
    time = route['time']
    miles = route['miles']
    highway = route['highway']
    
    slug = f"{from_city.lower().replace(' ', '-')}-to-{to_city.lower().replace(' ', '-')}"
    
    if slug in processed:
        continue
    processed.add(slug)
    
    reverse_slug = f"{to_city.lower().replace(' ', '-')}-to-{from_city.lower().replace(' ', '-')}"
    km = int(miles * 1.6)
    gallons = round(miles / 30, 1)
    gas_cost = int(gallons * 3.5)
    tolls = 10 if miles < 150 else (20 if miles < 300 else (35 if miles < 500 else 50))
    total_cost = gas_cost + tolls
    hours = 0
    if 'h' in time:
        parts = time.replace('min', '').split('h')
        hours = int(parts[0]) + (int(parts[1].strip()) / 60 if len(parts) > 1 and parts[1].strip() else 0)
    avg_speed = int(miles / hours) if hours > 0 else 65
    
    os.makedirs(f'route/{slug}', exist_ok=True)
    
    html = template.format(
        from_city=from_city, to_city=to_city, time=time, miles=miles,
        highway=highway, slug=slug, reverse_slug=reverse_slug, km=km,
        gallons=gallons, gas_cost=gas_cost, tolls=tolls, total_cost=total_cost, avg_speed=avg_speed
    )
    
    with open(f'route/{slug}/index.html', 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Updated {count} route pages")
