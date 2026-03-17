import os

# Get all cities
cities = sorted([d for d in os.listdir('cities') if os.path.isdir(f'cities/{d}')])
city_count = len(cities)

# Group by first letter
by_letter = {}
for city in cities:
    letter = city[0].upper()
    if letter not in by_letter:
        by_letter[letter] = []
    by_letter[letter].append(city)

# Popular cities to feature
popular = ['new-york', 'los-angeles', 'chicago', 'houston', 'phoenix', 'philadelphia', 
           'san-antonio', 'san-diego', 'dallas', 'san-jose', 'austin', 'jacksonville',
           'san-francisco', 'seattle', 'denver', 'boston', 'atlanta', 'miami', 
           'las-vegas', 'orlando', 'tampa', 'portland', 'nashville-tn', 'new-orleans']

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cities - Driving Routes | HowLongDrive</title>
    <meta name="description" content="Find driving routes from {city_count} US cities. Calculate drive times, distances, and gas costs.">
    <link rel="canonical" href="https://howlongdrive.com/cities/">
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
        .stat {{ font-size: 1.25rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem; }}
        .search-box {{ background: var(--card); padding: 1rem; border-radius: 0.75rem; margin-bottom: 2rem; }}
        .search-input {{ width: 100%; padding: 0.875rem 1rem; border: 2px solid var(--border); border-radius: 0.5rem; font-size: 1rem; }}
        .search-input:focus {{ outline: none; border-color: var(--primary); }}
        .section {{ margin-bottom: 2rem; }}
        .section h2 {{ font-size: 1rem; margin-bottom: 1rem; color: var(--muted); border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }}
        .cities-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.5rem; }}
        .city-card {{ background: var(--card); border-radius: 0.5rem; padding: 0.75rem 1rem; text-decoration: none; color: inherit; border: 1px solid var(--border); transition: all 0.15s; }}
        .city-card:hover {{ border-color: var(--primary); background: #f0f9ff; }}
        .city-name {{ font-weight: 500; font-size: 0.9rem; }}
        .letter-nav {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2rem; }}
        .letter-nav a {{ padding: 0.5rem 0.75rem; background: var(--card); border-radius: 0.25rem; text-decoration: none; color: var(--primary); font-weight: 600; border: 1px solid var(--border); }}
        .letter-nav a:hover {{ background: var(--primary); color: white; }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; }}
        .hidden {{ display: none !important; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","G-NXC7PNTC4G")</script>
</head>
<body>
    <header><div class="container header-inner">
        <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
        <nav><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/ev/" class="ev-badge">⚡ EV</a></nav>
    </div></header>
    <main class="container">
        <h1>🏙️ Cities</h1>
        <p class="subtitle">Find driving routes from {city_count} US cities</p>
        <div class="stat">{city_count} Cities</div>
        <div class="search-box">
            <input type="text" class="search-input" placeholder="Search cities..." id="search" onkeyup="filterCities()">
        </div>
        <div class="section">
            <h2>🔥 Popular Cities</h2>
            <div class="cities-grid">
'''

for city in popular:
    if city in cities:
        title = city.replace('-', ' ').title()
        html += f'                <a href="/cities/{city}/" class="city-card"><span class="city-name">{title}</span></a>\n'

html += '''            </div>
        </div>
        <div class="letter-nav">
'''

for letter in sorted(by_letter.keys()):
    html += f'            <a href="#letter-{letter}">{letter}</a>\n'

html += '''        </div>
'''

for letter in sorted(by_letter.keys()):
    html += f'''        <div class="section" id="letter-{letter}">
            <h2>{letter}</h2>
            <div class="cities-grid">
'''
    for city in by_letter[letter][:30]:  # Limit per letter for page size
        title = city.replace('-', ' ').title()
        html += f'                <a href="/cities/{city}/" class="city-card" data-city="{city}"><span class="city-name">{title}</span></a>\n'
    html += '''            </div>
        </div>
'''

html += '''    </main>
    <footer>© 2026 <a href="/">HowLongDrive.com</a></footer>
    <script>
        function filterCities() {
            const q = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.city-card').forEach(card => {
                const city = card.dataset.city || '';
                card.classList.toggle('hidden', q && !city.includes(q));
            });
        }
    </script>
</body>
</html>'''

with open('cities/index.html', 'w') as f:
    f.write(html)

print(f"✅ Updated cities/index.html with {city_count} cities")
