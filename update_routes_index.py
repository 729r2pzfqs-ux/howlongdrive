import os
from collections import defaultdict

# Count routes
route_count = len([d for d in os.listdir('route') if os.path.isdir(f'route/{d}')])
ev_count = len([d for d in os.listdir('ev') if os.path.isdir(f'ev/{d}')])
city_count = len([d for d in os.listdir('cities') if os.path.isdir(f'cities/{d}')])

# Get popular routes (sample)
popular_routes = []
sample_routes = [
    ('new-york-to-los-angeles', 'New York', 'Los Angeles', '40h', '2,775 mi'),
    ('los-angeles-to-las-vegas', 'Los Angeles', 'Las Vegas', '4h', '270 mi'),
    ('new-york-to-boston', 'New York', 'Boston', '4h', '215 mi'),
    ('chicago-to-new-york', 'Chicago', 'New York', '12h', '790 mi'),
    ('miami-to-orlando', 'Miami', 'Orlando', '3h 30m', '235 mi'),
    ('san-francisco-to-los-angeles', 'San Francisco', 'Los Angeles', '6h', '380 mi'),
    ('dallas-to-houston', 'Dallas', 'Houston', '3h 30m', '240 mi'),
    ('seattle-to-portland', 'Seattle', 'Portland', '3h', '175 mi'),
    ('denver-co-to-las-vegas', 'Denver', 'Las Vegas', '10h', '750 mi'),
    ('atlanta-to-miami', 'Atlanta', 'Miami', '10h', '660 mi'),
    ('boston-to-washington-dc', 'Boston', 'Washington DC', '7h 30m', '440 mi'),
    ('phoenix-to-los-angeles', 'Phoenix', 'Los Angeles', '5h 30m', '370 mi'),
]

# National parks routes
parks_routes = [
    ('los-angeles-to-grand-canyon', 'Los Angeles', 'Grand Canyon', '7h', '450 mi'),
    ('denver-to-yellowstone', 'Denver', 'Yellowstone', '8h', '525 mi'),
    ('san-francisco-to-yosemite', 'San Francisco', 'Yosemite', '3h', '170 mi'),
    ('seattle-to-glacier', 'Seattle', 'Glacier NP', '9h', '550 mi'),
    ('las-vegas-to-zion', 'Las Vegas', 'Zion NP', '2h 30m', '160 mi'),
    ('boston-to-acadia', 'Boston', 'Acadia NP', '4h 30m', '280 mi'),
]

print(f"Routes: {route_count}, EV: {ev_count}, Cities: {city_count}")

# Generate the HTML
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driving Routes & Road Trips | HowLongDrive</title>
    <meta name="description" content="Find driving times for {route_count}+ routes across the USA. Calculate drive time, gas costs, and plan road trips.">
    <link rel="canonical" href="https://howlongdrive.com/routes/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#4B6E93">
    <style>
        :root {{ --primary: #4B6E93; --green: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo img {{ height: 180px; }}
        nav {{ display: flex; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--green); color: #fff; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; }}
        @media (max-width: 768px) {{ .logo img {{ height: 144px; }} nav {{ display: none; }} }}
        h1 {{ font-size: 2rem; margin: 2rem 0 0.5rem; }}
        .subtitle {{ color: var(--muted); margin-bottom: 1.5rem; }}
        .stats {{ display: flex; gap: 2rem; margin: 1rem 0 2rem; flex-wrap: wrap; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; color: var(--primary); }}
        .stat-label {{ font-size: 0.8rem; color: var(--muted); }}
        .search-box {{ background: var(--card); padding: 1rem; border-radius: 0.75rem; margin-bottom: 2rem; }}
        .search-input {{ width: 100%; padding: 0.875rem 1rem; border: 2px solid var(--border); border-radius: 0.5rem; font-size: 1rem; }}
        .search-input:focus {{ outline: none; border-color: var(--primary); }}
        .section {{ margin-bottom: 2.5rem; }}
        .section h2 {{ font-size: 1.1rem; margin-bottom: 1rem; color: var(--text); }}
        .routes-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem; }}
        .route-card {{ background: var(--card); border-radius: 0.5rem; padding: 1rem; text-decoration: none; color: inherit; border: 1px solid var(--border); transition: border-color 0.15s; }}
        .route-card:hover {{ border-color: var(--primary); }}
        .route-title {{ font-weight: 600; font-size: 0.95rem; }}
        .route-meta {{ color: var(--muted); font-size: 0.8rem; margin-top: 0.25rem; }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G")</script>
</head>
<body>
    <header><div class="container header-inner">
        <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
        <nav><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/ev/" class="ev-badge">⚡ EV</a></nav>
    </div></header>
    <main class="container">
        <h1>🚗 Driving Routes</h1>
        <p class="subtitle">Find driving times and distances for {route_count:,}+ routes across the USA</p>
        <div class="stats">
            <div class="stat"><div class="stat-value">{route_count:,}</div><div class="stat-label">Routes</div></div>
            <div class="stat"><div class="stat-value">{ev_count:,}</div><div class="stat-label">EV Routes</div></div>
            <div class="stat"><div class="stat-value">{city_count}</div><div class="stat-label">Cities</div></div>
        </div>
        <div class="search-box">
            <input type="text" class="search-input" placeholder="Search routes (e.g., New York to Los Angeles)..." id="search">
        </div>
        <div class="section">
            <h2>🔥 Popular Routes</h2>
            <div class="routes-grid">
'''

for slug, from_city, to_city, time, dist in sample_routes:
    html += f'''                <a href="/route/{slug}/" class="route-card">
                    <div class="route-title">{from_city} → {to_city}</div>
                    <div class="route-meta">{time} • {dist}</div>
                </a>
'''

html += '''            </div>
        </div>
        <div class="section">
            <h2>🏞️ National Parks</h2>
            <div class="routes-grid">
'''

for slug, from_city, to_city, time, dist in parks_routes:
    html += f'''                <a href="/route/{slug}/" class="route-card">
                    <div class="route-title">{from_city} → {to_city}</div>
                    <div class="route-meta">{time} • {dist}</div>
                </a>
'''

html += '''            </div>
        </div>
    </main>
    <footer>© 2026 <a href="/">HowLongDrive.com</a></footer>
</body>
</html>'''

with open('routes/index.html', 'w') as f:
    f.write(html)

print("✅ Updated routes/index.html")
