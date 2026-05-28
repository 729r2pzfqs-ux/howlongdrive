#!/usr/bin/env python3
"""
Fix two Semrush AI Search Health issues:
1. Low word count on route/city/EV pages - add templated content
2. Low semantic HTML usage on top-level pages
"""

import os
import re
import hashlib
import glob

REPO = '/sessions/sharp-zen-bohr/mnt/outputs/howlongdrive'

# ============================================================
# ISSUE 1: LOW WORD COUNT - Add content to route/city/EV pages
# ============================================================

def slug_to_name(slug):
    """Convert a URL slug to a readable name."""
    # Handle state abbreviations
    state_map = {
        'al': 'AL', 'ak': 'AK', 'az': 'AZ', 'ar': 'AR', 'ca': 'CA',
        'co': 'CO', 'ct': 'CT', 'de': 'DE', 'fl': 'FL', 'ga': 'GA',
        'hi': 'HI', 'id': 'ID', 'il': 'IL', 'in': 'IN', 'ia': 'IA',
        'ks': 'KS', 'ky': 'KY', 'la': 'LA', 'me': 'ME', 'md': 'MD',
        'ma': 'MA', 'mi': 'MI', 'mn': 'MN', 'ms': 'MS', 'mo': 'MO',
        'mt': 'MT', 'ne': 'NE', 'nv': 'NV', 'nh': 'NH', 'nj': 'NJ',
        'nm': 'NM', 'ny': 'NY', 'nc': 'NC', 'nd': 'ND', 'oh': 'OH',
        'ok': 'OK', 'or': 'OR', 'pa': 'PA', 'ri': 'RI', 'sc': 'SC',
        'sd': 'SD', 'tn': 'TN', 'tx': 'TX', 'ut': 'UT', 'vt': 'VT',
        'va': 'VA', 'wa': 'WA', 'wv': 'WV', 'wi': 'WI', 'wy': 'WY',
        'dc': 'DC',
    }
    parts = slug.split('-')
    result = []
    for p in parts:
        if p.lower() in state_map:
            result.append(state_map[p.lower()])
        elif p.lower() in ('osu',):
            result.append(p.upper())
        else:
            result.append(p.capitalize())
    return ' '.join(result)

def extract_route_data(html):
    """Extract origin, destination, time, distance, gas cost, route from HTML."""
    data = {}
    # Extract from title
    title_m = re.search(r'<title>([^<]+)</title>', html)
    if title_m:
        data['title'] = title_m.group(1)
    
    # Extract stat values
    stats = re.findall(r'stat-value">([^<]+)', html)
    if len(stats) >= 3:
        data['time'] = stats[0]
        data['distance'] = stats[1]
        data['gas_cost'] = stats[2]
    if len(stats) >= 4:
        data['tolls'] = stats[3]
    
    # Extract route name (via ...)
    route_m = re.search(r'class="subtitle">via ([^<]+)', html)
    if route_m:
        data['route'] = route_m.group(1)
    
    # Extract suggested stops
    stops = re.findall(r'📍 ([^<]+)', html)
    data['stops'] = stops
    
    # Extract best time
    best_m = re.search(r'Best Time</span><span>([^<]+)', html)
    if best_m:
        data['best_time'] = best_m.group(1)
    
    return data

def pick_variant(seed, count):
    """Pick a deterministic variant based on seed string."""
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return h % count

def generate_route_content(origin, dest, data, seed):
    """Generate 1-2 paragraphs of driving content for route pages. 4 variants."""
    time = data.get('time', 'a few hours')
    dist = data.get('distance', 'several miles')
    route = data.get('route', 'the highway')
    gas = data.get('gas_cost', '$30')
    stops = data.get('stops', [])
    best_time = data.get('best_time', 'early morning')
    
    # Parse distance number for trip classification
    dist_num = 0
    try:
        dist_num = int(re.sub(r'[^\d]', '', str(dist)))
    except:
        pass
    
    if dist_num < 100:
        trip_type = "short drive"
        tip_text_options = [
            f"At just {dist} miles, this is a comfortable day trip that won't require any fuel stops along the way. You can easily make the round trip in a single day with plenty of time to spare.",
            f"This {dist}-mile journey is short enough to complete without breaking a sweat. Consider combining it with nearby attractions or turning it into a scenic afternoon drive.",
            f"Covering only {dist} miles, this quick trip is ideal for a day outing. Most drivers find the route straightforward, with no need for rest stops unless you prefer a leisurely pace.",
            f"With a distance of {dist} miles, you can be at your destination in well under two hours. It's a great option for a spontaneous weekend excursion without the hassle of an overnight stay.",
        ]
    elif dist_num < 400:
        trip_type = "moderate drive"
        tip_text_options = [
            f"Covering {dist} miles, this is a solid half-day drive. Pack some snacks and a good playlist — you'll want to stay comfortable for the journey. A single fuel stop should be sufficient for most vehicles.",
            f"At {dist} miles, plan for a comfortable drive with one or two rest stops along the way. This distance is manageable in a single stretch for experienced drivers, but taking breaks helps you arrive refreshed.",
            f"This {dist}-mile route is long enough to merit some planning. Bring water and snacks, check your tire pressure before departure, and consider splitting the drive with a co-driver if you prefer company.",
            f"The {dist}-mile distance makes this a proper road trip. Start with a full tank, grab a coffee for the road, and enjoy the changing scenery as you make your way from {origin} to {dest}.",
        ]
    else:
        trip_type = "long road trip"
        tip_text_options = [
            f"This is a serious {dist}-mile road trip that spans multiple states and regions. Plan for at least one overnight stop, pack emergency supplies, and make sure your vehicle is road-trip ready with fresh oil and properly inflated tires.",
            f"At {dist} miles, this cross-country journey deserves careful planning. Consider breaking it into two or more days, booking hotels along the route, and mapping out fuel stops in advance — especially through rural stretches.",
            f"Covering {dist} miles, this epic drive takes you across a huge swath of the country. Prepare for varied weather conditions, different speed limits by state, and long stretches between services. A well-planned itinerary makes all the difference.",
            f"This {dist}-mile trek is a true American road trip. Stock up on audiobooks or podcasts, rotate drivers if possible, and build in time for roadside attractions. The journey itself is part of the adventure.",
        ]
    
    variant = pick_variant(seed, 4)
    
    main_paragraphs = [
        f'<p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">The {trip_type} from {origin} to {dest} follows {route} for {dist} miles, with an estimated travel time of {time} under normal conditions. Fuel costs run approximately {gas} at current prices, assuming average fuel efficiency of 30 MPG. {best_time.capitalize()} is generally the best window to depart for the smoothest ride.</p>',
        f'<p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">Heading from {origin} to {dest}? This {dist}-mile {trip_type} via {route} takes roughly {time} in typical traffic. Budget around {gas} for gas, and aim to leave during {best_time.lower()} to minimize delays and enjoy a stress-free drive.</p>',
        f'<p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">Planning a trip from {origin} to {dest}? The most common route runs along {route}, covering {dist} miles in about {time}. Gas will set you back roughly {gas} for the one-way trip. For the best experience, hit the road during {best_time.lower()} when traffic is lightest.</p>',
        f'<p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">The journey from {origin} to {dest} stretches {dist} miles along {route} and typically takes {time} to complete. At today\'s fuel prices, expect to spend around {gas} on gas. Departing during {best_time.lower()} gives you the best chance of avoiding congestion along the way.</p>',
    ]
    
    tip_text = tip_text_options[variant]
    
    stops_text = ""
    if stops:
        stops_str = ", ".join(stops[:3])
        stops_text = f" Popular stopping points include {stops_str} — great options for grabbing a meal, fueling up, or stretching your legs."
    
    content = main_paragraphs[variant]
    content += f'\n            <p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">{tip_text}{stops_text}</p>'
    
    return content

def generate_ev_content(origin, dest, data, seed):
    """Generate EV-specific content. 4 variants."""
    time = data.get('time', 'a few hours')
    dist = data.get('distance', 'several miles')
    stops = data.get('stops', '0')
    ev_cost = data.get('ev_cost', '$10')
    gas_cost = data.get('gas_cost', '$25')
    savings = data.get('savings', '$15')
    
    dist_num = 0
    try:
        dist_num = int(re.sub(r'[^\d]', '', str(dist)))
    except:
        pass
    
    variant = pick_variant(seed, 4)
    
    if dist_num <= 250:
        range_text_options = [
            f"At {dist} miles, most modern EVs with a 250+ mile range can complete this trip on a single charge without any stops. Top off your battery before you leave and you should arrive with charge to spare.",
            f"This {dist}-mile route falls comfortably within the range of most current electric vehicles. You can likely make it door-to-door without needing to stop for a charge, though having a charging plan is always wise.",
            f"Good news for EV drivers: at {dist} miles, this trip is well within single-charge range for most battery electric vehicles on the market today. Pre-condition your battery before departure for optimal efficiency.",
            f"With a distance of {dist} miles, this route is EV-friendly right out of the gate. Most electric cars with a range of 250 miles or more will handle this comfortably on one full charge.",
        ]
    else:
        stops_num = max(1, (dist_num - 200) // 150)
        range_text_options = [
            f"Covering {dist} miles, this EV road trip will require approximately {stops_num} charging stop{'s' if stops_num > 1 else ''} for most electric vehicles. Plan your stops around DC fast chargers along {data.get('route', 'the highway')} — a 20-30 minute fast charge can add 150+ miles of range.",
            f"This {dist}-mile journey means you'll need to plan for {stops_num} charging stop{'s' if stops_num > 1 else ''}. Apps like PlugShare or your vehicle's built-in trip planner can help locate the best DC fast chargers along the route and estimate wait times.",
            f"At {dist} miles, expect to make around {stops_num} charging stop{'s' if stops_num > 1 else ''} during this EV trip. Time your stops with meal breaks or rest stops to make the most of charging downtime. Most DC fast chargers will get you back on the road in under 30 minutes.",
            f"For this {dist}-mile drive, EV owners should plan on {stops_num} charging stop{'s' if stops_num > 1 else ''}. Check charger availability ahead of time, especially on holiday weekends when popular stations can get busy. Having a backup charger location in mind is always a good idea.",
        ]
    
    range_text = range_text_options[variant]
    
    cost_text_options = [
        f"Driving electric from {origin} to {dest} costs approximately {ev_cost} in electricity, compared to {gas_cost} for a gas vehicle — a savings of {savings}. Over multiple trips, those savings add up significantly.",
        f"One of the biggest perks of this EV trip: fuel savings. You'll spend roughly {ev_cost} on electricity versus {gas_cost} at the pump, keeping {savings} in your pocket. Charging at home overnight is even cheaper than using public fast chargers.",
        f"The cost advantage of going electric is clear on this route: about {ev_cost} for electricity versus {gas_cost} for gasoline, saving you {savings} each way. If you charge at home before departing, your per-mile cost drops even further.",
        f"Electric driving shines on this route with estimated energy costs of just {ev_cost}, compared to {gas_cost} for a conventional vehicle. That {savings} in savings per trip makes a real difference for frequent travelers.",
    ]
    
    content = f'<p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">{range_text}</p>'
    content += f'\n            <p style="color:var(--muted);font-size:0.9rem;line-height:1.7;margin-top:0.75rem">{cost_text_options[variant]}</p>'
    
    return content

def generate_city_content(city_name, num_destinations, seed):
    """Generate a paragraph about driving from a city. 4 variants."""
    variant = pick_variant(seed, 4)
    
    texts = [
        f'<section style="margin-top:1.5rem;padding:1.5rem;background:var(--card);border-radius:0.75rem;box-shadow:0 1px 3px rgba(0,0,0,0.08)"><h2 style="font-size:1.1rem;margin-bottom:0.75rem;color:var(--primary)">Driving from {city_name}</h2><p style="color:var(--muted);font-size:0.9rem;line-height:1.7">{city_name} is a popular starting point for road trips across the United States, with {num_destinations} destinations reachable by car. Whether you are planning a quick day trip to a neighboring city or an extended cross-country adventure, this page provides accurate driving times, distances, and estimated fuel costs for every route. Use the cards above to compare drive times and pick the best destination for your next trip. Each route page includes detailed information about highway options, toll costs, traffic patterns, and the best times to travel.</p></section>',
        f'<section style="margin-top:1.5rem;padding:1.5rem;background:var(--card);border-radius:0.75rem;box-shadow:0 1px 3px rgba(0,0,0,0.08)"><h2 style="font-size:1.1rem;margin-bottom:0.75rem;color:var(--primary)">Road Trips from {city_name}</h2><p style="color:var(--muted);font-size:0.9rem;line-height:1.7">Looking to hit the road from {city_name}? Browse {num_destinations} driving routes with detailed travel data including estimated drive times, mileage, and gas costs. From short trips under an hour to epic multi-day drives, {city_name} connects to destinations across the country. Click any route card for a full breakdown of the journey, including suggested stops, traffic estimates, toll information, and the recommended time of day to depart for the smoothest drive.</p></section>',
        f'<section style="margin-top:1.5rem;padding:1.5rem;background:var(--card);border-radius:0.75rem;box-shadow:0 1px 3px rgba(0,0,0,0.08)"><h2 style="font-size:1.1rem;margin-bottom:0.75rem;color:var(--primary)">Explore Routes from {city_name}</h2><p style="color:var(--muted);font-size:0.9rem;line-height:1.7">From {city_name}, you can drive to {num_destinations} different cities and attractions across the US. This page lists every available route sorted by distance, making it easy to find both nearby getaways and faraway adventures. Each destination card shows the driving distance and estimated travel time at a glance. Click through to any route for in-depth details on highway options, fuel expenses, rest stop suggestions, and real-time traffic considerations to help you plan the perfect trip.</p></section>',
        f'<section style="margin-top:1.5rem;padding:1.5rem;background:var(--card);border-radius:0.75rem;box-shadow:0 1px 3px rgba(0,0,0,0.08)"><h2 style="font-size:1.1rem;margin-bottom:0.75rem;color:var(--primary)">Plan Your Drive from {city_name}</h2><p style="color:var(--muted);font-size:0.9rem;line-height:1.7">{city_name} serves as a great base for exploring by car, with {num_destinations} routes available on this page. Whether you need a quick commute estimate or want to map out a weekend road trip, you will find driving times and costs for every destination below. Each route includes up-to-date data on distance, fuel estimates at current prices, toll costs where applicable, and recommendations for the best departure times. Tap any card to see the full route details and start planning your drive.</p></section>',
    ]
    
    return texts[variant]


def process_route_pages():
    """Add content to route pages."""
    count = 0
    route_dirs = glob.glob(os.path.join(REPO, 'route', '*'))
    for rdir in route_dirs:
        fpath = os.path.join(rdir, 'index.html')
        if not os.path.isfile(fpath):
            continue
        
        # Extract origin-dest from dir name
        dirname = os.path.basename(rdir)
        parts = dirname.split('-to-')
        if len(parts) != 2:
            continue
        origin = slug_to_name(parts[0])
        dest = slug_to_name(parts[1])
        
        with open(fpath, 'r') as f:
            html = f.read()
        
        # Check if we already added content (idempotency)
        if 'driving-tips-section' in html:
            continue
        
        data = extract_route_data(html)
        data['route'] = data.get('route', 'the highway')
        
        content = generate_route_content(origin, dest, data, dirname)
        
        # Insert before the related-section
        section_html = f'''
        <div class="card driving-tips-section" style="margin-top:1rem">
            <h3 style="margin-bottom:0.75rem;display:flex;align-items:center;gap:0.5rem"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;color:var(--primary)"><path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/></svg> Driving Tips: {origin} to {dest}</h3>
            {content}
        </div>
'''
        
        # Insert before related-section
        if '<div class="related-section">' in html:
            html = html.replace('<div class="related-section">', section_html + '    <div class="related-section">', 1)
        else:
            # Insert before footer
            html = html.replace('    <footer', section_html + '    <footer', 1)
        
        with open(fpath, 'w') as f:
            f.write(html)
        count += 1
    
    return count

def process_ev_pages():
    """Add EV-specific content to EV pages."""
    count = 0
    ev_dirs = glob.glob(os.path.join(REPO, 'ev', '*'))
    for edir in ev_dirs:
        fpath = os.path.join(edir, 'index.html')
        if not os.path.isfile(fpath):
            continue
        
        dirname = os.path.basename(edir)
        parts = dirname.split('-to-')
        if len(parts) != 2:
            continue
        origin = slug_to_name(parts[0])
        dest = slug_to_name(parts[1])
        
        with open(fpath, 'r') as f:
            html = f.read()
        
        if 'ev-tips-section' in html:
            continue
        
        # Extract EV-specific data
        data = {}
        stats = re.findall(r'stat-value">([^<]+)', html)
        if len(stats) >= 4:
            data['distance'] = stats[0]
            data['stops'] = stats[1]
            data['time'] = stats[2]
            data['ev_cost'] = stats[3]
        
        # Extract gas cost and savings
        gas_m = re.search(r'Gas</span><span>(\$[\d]+)', html)
        if gas_m:
            data['gas_cost'] = gas_m.group(1)
        save_m = re.search(r'Save</span><span[^>]*>(\$[\d]+)', html)
        if save_m:
            data['savings'] = save_m.group(1)
        
        route_m = re.search(r'subtitle">([^<]+)', html)
        if route_m:
            data['route'] = route_m.group(1)
        
        content = generate_ev_content(origin, dest, data, dirname)
        
        section_html = f'''
        <div class="card ev-tips-section" style="margin-top:1rem">
            <h3 style="margin-bottom:0.75rem;display:flex;align-items:center;gap:0.5rem"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;color:var(--primary)"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> EV Charging Guide: {origin} to {dest}</h3>
            {content}
        </div>
'''
        
        if '<div class="related-section">' in html:
            html = html.replace('<div class="related-section">', section_html + '    <div class="related-section">', 1)
        elif '    <footer' in html:
            html = html.replace('    <footer', section_html + '    <footer', 1)
        
        with open(fpath, 'w') as f:
            f.write(html)
        count += 1
    
    return count

def process_city_pages():
    """Add content to city pages."""
    count = 0
    city_dirs = glob.glob(os.path.join(REPO, 'city', '*'))
    for cdir in city_dirs:
        fpath = os.path.join(cdir, 'index.html')
        if not os.path.isfile(fpath):
            continue
        
        dirname = os.path.basename(cdir)
        city_name = slug_to_name(dirname)
        
        with open(fpath, 'r') as f:
            html = f.read()
        
        if 'city-info-section' in html:
            continue
        
        # Count destinations
        num_dest = len(re.findall(r'route-card', html))
        
        content = generate_city_content(city_name, num_dest, dirname)
        # Add class marker
        content = content.replace('<section', '<section class="city-info-section"', 1)
        
        # Insert before footer
        if '<footer' in html:
            html = html.replace('<footer', content + '\n<footer', 1)
        
        with open(fpath, 'w') as f:
            f.write(html)
        count += 1
    
    return count

# Also handle cities/ pages (different from city/)
def process_cities_pages():
    """Add content to cities/ subdirectory pages."""
    count = 0
    cities_dirs = glob.glob(os.path.join(REPO, 'cities', '*'))
    for cdir in cities_dirs:
        if not os.path.isdir(cdir):
            continue
        fpath = os.path.join(cdir, 'index.html')
        if not os.path.isfile(fpath):
            continue
        
        dirname = os.path.basename(cdir)
        city_name = slug_to_name(dirname)
        
        with open(fpath, 'r') as f:
            html = f.read()
        
        if 'city-info-section' in html:
            continue
        
        num_dest = len(re.findall(r'route-card', html))
        
        content = generate_city_content(city_name, num_dest, dirname)
        content = content.replace('<section', '<section class="city-info-section"', 1)
        
        if '<footer' in html:
            html = html.replace('<footer', content + '\n<footer', 1)
        
        with open(fpath, 'w') as f:
            f.write(html)
        count += 1
    
    return count


# ============================================================
# ISSUE 2: SEMANTIC HTML - Fix top-level pages
# ============================================================

def fix_semantic_about():
    """Fix about page semantic HTML."""
    fpath = os.path.join(REPO, 'about', 'index.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    if '<main' in html:
        return False
    
    # Wrap main content div in <main> and <article>
    html = html.replace(
        '<div class="container">\n        <div class="content">',
        '<main class="container">\n        <article class="content">'
    )
    # Close them - find the contact-box closing and footer
    html = html.replace(
        '</div>\n    </div>\n    \n    <footer',
        '</div>\n    </article>\n    </main>\n    \n    <footer'
    )
    
    with open(fpath, 'w') as f:
        f.write(html)
    return True

def fix_semantic_privacy():
    """Fix privacy page semantic HTML."""
    fpath = os.path.join(REPO, 'privacy.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    if '<main' in html:
        return False
    
    html = html.replace(
        '<div class="container content">',
        '<main class="container content">'
    )
    # Find the closing div before footer
    # The content div closes right before footer
    html = re.sub(
        r'</div>\s*<footer',
        '</main>\n<footer',
        html,
        count=1
    )
    
    with open(fpath, 'w') as f:
        f.write(html)
    return True

def fix_semantic_terms():
    """Fix terms page semantic HTML."""
    fpath = os.path.join(REPO, 'terms.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    if '<main' in html:
        return False
    
    html = html.replace(
        '<div class="container content">',
        '<main class="container content">'
    )
    html = re.sub(
        r'</div>\s*<footer',
        '</main>\n<footer',
        html,
        count=1
    )
    
    with open(fpath, 'w') as f:
        f.write(html)
    return True

def fix_semantic_guides():
    """Fix guides page semantic HTML."""
    fpath = os.path.join(REPO, 'guides', 'index.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    if '<main' in html:
        return False
    
    # Wrap the container div after header in <main>
    html = html.replace(
        '    <div class="container">\n        <h1>',
        '    <main class="container">\n        <h1>'
    )
    # Find closing container div before footer
    # The guides container ends before footer
    html = re.sub(
        r'</div>\s*\n\s*<footer',
        '</main>\n    <footer',
        html,
        count=1
    )
    
    with open(fpath, 'w') as f:
        f.write(html)
    return True

def fix_semantic_ev_index():
    """Fix EV index page semantic HTML."""
    fpath = os.path.join(REPO, 'ev', 'index.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    if '<main' in html:
        return False
    
    html = html.replace(
        '    <div class="container">\n        <div class="hero">',
        '    <main class="container">\n        <section class="hero">'
    )
    # Fix closing hero div
    # Find the search box closing and stats section
    # This is trickier - let's wrap the outer container
    # Actually, simpler: just change the outer container div to main
    # Revert and do simpler approach
    fpath = os.path.join(REPO, 'ev', 'index.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    # Simple approach: replace first <div class="container"> after </header> with <main>
    # Split at </header>
    parts = html.split('</header>', 1)
    if len(parts) == 2:
        after = parts[1]
        after = after.replace('<div class="container">', '<main class="container">', 1)
        # Replace the last </div> before <footer with </main>
        footer_idx = after.rfind('<footer')
        if footer_idx > 0:
            # Find the </div> right before footer
            last_div = after.rfind('</div>', 0, footer_idx)
            if last_div > 0:
                after = after[:last_div] + '</main>' + after[last_div+6:]
        html = parts[0] + '</header>' + after
    
    with open(fpath, 'w') as f:
        f.write(html)
    return True

def fix_semantic_404():
    """Fix 404 page - already has main, check for article."""
    fpath = os.path.join(REPO, '404.html')
    with open(fpath, 'r') as f:
        html = f.read()
    
    # Already has <main>, check if needs article
    if '<article' in html:
        return False
    
    # 404 is simple, probably fine as-is
    return False


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=== Issue 1: Adding content to low word count pages ===")
    
    n = process_route_pages()
    print(f"Route pages updated: {n}")
    
    n = process_ev_pages()
    print(f"EV pages updated: {n}")
    
    n = process_city_pages()
    print(f"City pages updated: {n}")
    
    n = process_cities_pages()
    print(f"Cities pages updated: {n}")
    
    print("\n=== Issue 2: Fixing semantic HTML ===")
    
    pages = [
        ('about/index.html', fix_semantic_about),
        ('privacy.html', fix_semantic_privacy),
        ('terms.html', fix_semantic_terms),
        ('guides/index.html', fix_semantic_guides),
        ('ev/index.html', fix_semantic_ev_index),
        ('404.html', fix_semantic_404),
    ]
    
    for name, func in pages:
        result = func()
        print(f"  {name}: {'FIXED' if result else 'already OK / skipped'}")
    
    print("\nDone!")
