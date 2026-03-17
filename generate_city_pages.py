import os
import re
from collections import defaultdict

# Get all existing cities
existing_cities = set(os.listdir('cities'))

# Find all route pages and extract city pairs
city_routes = defaultdict(list)

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    
    # Parse slug: city1-to-city2
    if '-to-' in d:
        parts = d.split('-to-')
        if len(parts) == 2:
            from_city = parts[0]
            to_city = parts[1]
            city_routes[from_city].append((to_city, d))
            city_routes[to_city].append((from_city, d))

# Get missing cities
missing_cities = set(city_routes.keys()) - existing_cities
print(f"Missing cities to create: {len(missing_cities)}")

# City page template
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driving Routes from {city_title} | HowLongDrive</title>
    <meta name="description" content="Find driving times and distances from {city_title}. {route_count} routes available with gas costs and EV charging info.">
    <link rel="canonical" href="https://howlongdrive.com/cities/{city_slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#4B6E93">
    <style>
        :root {{ --primary: #4B6E93; --green: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ color: var(--primary); text-decoration: none; }}
        .logo img {{ height: 180px; }}
        nav {{ display: flex; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--green); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; }}
        @media (max-width: 768px) {{ .logo img {{ height: 144px; }} nav {{ display: none; }} }}
        .hero {{ background: linear-gradient(135deg, #4B6E93, #3a5775); padding: 2rem; border-radius: 1rem; margin: 1rem 0; color: white; }}
        h1 {{ font-size: 1.75rem; margin-bottom: 0.5rem; }}
        .subtitle {{ opacity: 0.9; }}
        .routes {{ display: grid; gap: 0.75rem; margin-top: 1.5rem; }}
        .route-card {{ background: var(--card); padding: 1rem 1.25rem; border-radius: 0.5rem; display: flex; justify-content: space-between; align-items: center; text-decoration: none; color: var(--text); box-shadow: 0 1px 3px rgba(0,0,0,0.08); transition: transform 0.2s; }}
        .route-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .route-dest {{ font-weight: 600; }}
        .route-info {{ color: var(--muted); font-size: 0.875rem; }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G");</script></head>
<body>
    <header><div class="container header-inner">
        <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
        <nav><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/ev/" class="ev-badge">⚡ EV</a></nav>
    </div></header>
    <main class="container">
        <div class="hero">
            <h1>🚗 Routes from {city_title}</h1>
            <p class="subtitle">{route_count} driving routes available</p>
        </div>
        <div class="routes">
{route_links}
        </div>
    </main>
    <footer>© 2026 HowLongDrive</footer>
</body>
</html>'''

# Generate pages for missing cities
count = 0
for city_slug in missing_cities:
    routes = city_routes[city_slug]
    if not routes:
        continue
    
    # Format city title
    city_title = city_slug.replace('-', ' ').title()
    
    # Generate route links
    route_links = []
    for dest, route_slug in sorted(routes, key=lambda x: x[0])[:50]:  # Limit to 50
        dest_title = dest.replace('-', ' ').title()
        route_links.append(f'            <a href="/route/{route_slug}/" class="route-card"><span class="route-dest">{dest_title}</span><span class="route-info">View route →</span></a>')
    
    html = TEMPLATE.format(
        city_title=city_title,
        city_slug=city_slug,
        route_count=len(routes),
        route_links='\n'.join(route_links)
    )
    
    os.makedirs(f'cities/{city_slug}', exist_ok=True)
    with open(f'cities/{city_slug}/index.html', 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Created {count} new city pages")
