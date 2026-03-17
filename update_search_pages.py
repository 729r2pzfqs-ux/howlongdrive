import os
import re

# Get all city slugs
cities = sorted([d for d in os.listdir('cities') if os.path.isdir(f'cities/{d}')])
city_names = [c.replace('-', ' ').title() for c in cities]

# Routes page with autocomplete
routes_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driving Routes & Road Trips | HowLongDrive</title>
    <meta name="description" content="Find driving times for 8,400+ routes across the USA. Calculate drive time, gas costs, and plan road trips.">
    <link rel="canonical" href="https://howlongdrive.com/routes/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
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
        h1 {{ font-size: 2rem; margin: 2rem 0 0.5rem; display: flex; align-items: center; gap: 0.75rem; }}
        h1 svg {{ width: 32px; height: 32px; color: var(--primary); }}
        .subtitle {{ color: var(--muted); margin-bottom: 1.5rem; }}
        .stats {{ display: flex; gap: 2rem; margin: 1rem 0 2rem; flex-wrap: wrap; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; color: var(--primary); }}
        .stat-label {{ font-size: 0.8rem; color: var(--muted); }}
        .search-box {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .search-row {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
        .input-wrapper {{ flex: 1; min-width: 200px; position: relative; }}
        .search-input {{ width: 100%; padding: 0.875rem 1rem; border: 2px solid var(--border); border-radius: 0.5rem; font-size: 1rem; }}
        .search-input:focus {{ outline: none; border-color: var(--primary); }}
        .dropdown {{ position: absolute; top: 100%; left: 0; right: 0; background: var(--card); border: 1px solid var(--border); border-radius: 0.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: none; z-index: 100; max-height: 250px; overflow-y: auto; }}
        .dropdown.active {{ display: block; }}
        .dropdown-item {{ padding: 0.75rem 1rem; cursor: pointer; border-bottom: 1px solid var(--border); }}
        .dropdown-item:last-child {{ border-bottom: none; }}
        .dropdown-item:hover {{ background: var(--bg); color: var(--primary); }}
        .search-btn {{ background: var(--primary); color: white; border: none; padding: 0.875rem 1.5rem; border-radius: 0.5rem; font-size: 1rem; font-weight: 600; cursor: pointer; margin-top: 1rem; }}
        .search-btn:hover {{ background: #3d5a7a; }}
        .section {{ margin-bottom: 2.5rem; }}
        .section h2 {{ font-size: 1.1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
        .section h2 svg {{ width: 20px; height: 20px; color: var(--primary); }}
        .routes-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem; }}
        .route-card {{ background: var(--card); border-radius: 0.5rem; padding: 1rem; text-decoration: none; color: inherit; border: 1px solid var(--border); }}
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
        <nav><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/guides/">Guides</a><a href="/ev/" class="ev-badge">⚡ EV Trips</a><a href="/about/">About</a></nav>
    </div></header>
    <main class="container">
        <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Driving Routes</h1>
        <p class="subtitle">Find driving times and distances for 8,400+ routes across the USA</p>
        <div class="stats">
            <div class="stat"><div class="stat-value">8,420</div><div class="stat-label">Routes</div></div>
            <div class="stat"><div class="stat-value">8,420</div><div class="stat-label">EV Routes</div></div>
            <div class="stat"><div class="stat-value">918</div><div class="stat-label">Cities</div></div>
        </div>
        <div class="search-box">
            <div class="search-row">
                <div class="input-wrapper">
                    <input type="text" class="search-input" placeholder="From (e.g., New York)" id="from" autocomplete="off">
                    <div class="dropdown" id="from-dropdown"></div>
                </div>
                <div class="input-wrapper">
                    <input type="text" class="search-input" placeholder="To (e.g., Los Angeles)" id="to" autocomplete="off">
                    <div class="dropdown" id="to-dropdown"></div>
                </div>
            </div>
            <button class="search-btn" onclick="search()">Get Driving Time</button>
        </div>
        <div class="section">
            <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Popular Routes</h2>
            <div class="routes-grid">
                <a href="/route/new-york-to-los-angeles/" class="route-card"><div class="route-title">New York → Los Angeles</div><div class="route-meta">40h • 2,775 mi</div></a>
                <a href="/route/los-angeles-to-las-vegas/" class="route-card"><div class="route-title">Los Angeles → Las Vegas</div><div class="route-meta">4h • 270 mi</div></a>
                <a href="/route/new-york-to-boston/" class="route-card"><div class="route-title">New York → Boston</div><div class="route-meta">4h • 215 mi</div></a>
                <a href="/route/chicago-to-new-york/" class="route-card"><div class="route-title">Chicago → New York</div><div class="route-meta">12h • 790 mi</div></a>
                <a href="/route/miami-to-orlando/" class="route-card"><div class="route-title">Miami → Orlando</div><div class="route-meta">3h 30m • 235 mi</div></a>
                <a href="/route/san-francisco-to-los-angeles/" class="route-card"><div class="route-title">San Francisco → Los Angeles</div><div class="route-meta">6h • 380 mi</div></a>
            </div>
        </div>
        <div class="section">
            <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3l4 8 5-5 5 15H2L8 3z"/></svg> National Parks</h2>
            <div class="routes-grid">
                <a href="/route/los-angeles-to-grand-canyon/" class="route-card"><div class="route-title">Los Angeles → Grand Canyon</div><div class="route-meta">7h • 450 mi</div></a>
                <a href="/route/denver-to-yellowstone/" class="route-card"><div class="route-title">Denver → Yellowstone</div><div class="route-meta">8h • 525 mi</div></a>
                <a href="/route/san-francisco-to-yosemite/" class="route-card"><div class="route-title">San Francisco → Yosemite</div><div class="route-meta">3h • 170 mi</div></a>
                <a href="/route/las-vegas-to-zion/" class="route-card"><div class="route-title">Las Vegas → Zion NP</div><div class="route-meta">2h 30m • 160 mi</div></a>
            </div>
        </div>
    </main>
    <footer>© 2026 <a href="/">HowLongDrive.com</a></footer>
    <script>
        const CITIES = {city_names};
        
        function setupAutocomplete(inputId, dropdownId) {{
            const input = document.getElementById(inputId);
            const dropdown = document.getElementById(dropdownId);
            
            input.addEventListener('input', function() {{
                const val = this.value.toLowerCase();
                dropdown.innerHTML = '';
                if (val.length < 1) {{ dropdown.classList.remove('active'); return; }}
                
                const matches = CITIES.filter(c => c.toLowerCase().includes(val)).slice(0, 8);
                if (matches.length === 0) {{ dropdown.classList.remove('active'); return; }}
                
                matches.forEach(city => {{
                    const div = document.createElement('div');
                    div.className = 'dropdown-item';
                    div.textContent = city;
                    div.onclick = () => {{ input.value = city; dropdown.classList.remove('active'); }};
                    dropdown.appendChild(div);
                }});
                dropdown.classList.add('active');
            }});
            
            document.addEventListener('click', e => {{
                if (!input.contains(e.target) && !dropdown.contains(e.target)) dropdown.classList.remove('active');
            }});
        }}
        
        setupAutocomplete('from', 'from-dropdown');
        setupAutocomplete('to', 'to-dropdown');
        
        function search() {{
            const from = document.getElementById('from').value.toLowerCase().replace(/[^a-z0-9]+/g, '-');
            const to = document.getElementById('to').value.toLowerCase().replace(/[^a-z0-9]+/g, '-');
            if (from && to) window.location.href = '/route/' + from + '-to-' + to + '/';
        }}
        
        document.getElementById('to').addEventListener('keydown', e => {{
            if (e.key === 'Enter') search();
        }});
    </script>
</body>
</html>'''

with open('routes/index.html', 'w') as f:
    f.write(routes_html)

print("✅ Updated routes/index.html with autocomplete")
