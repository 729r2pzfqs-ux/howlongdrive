import os
import re

count = 0

for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Get actual drive time from details row
    drive_match = re.search(r'<span>Drive Time</span><span>(\d+)\s*(min|h)', html)
    if not drive_match:
        continue
    
    drive_val = drive_match.group(1)
    drive_unit = drive_match.group(2)
    
    if drive_unit == 'min':
        # It's minutes - format as 0h Xm
        mins = int(drive_val)
        if mins < 60:
            time_str = f"0h {mins}m"
        else:
            h = mins // 60
            m = mins % 60
            time_str = f"{h}h {m}m"
    else:
        # It's hours - keep the format from the row
        # Need to parse better, check for full format
        full_match = re.search(r'<span>Drive Time</span><span>(\d+)h\s*(\d+)?m?i?n?</span>', html)
        if full_match:
            h = int(full_match.group(1))
            m = int(full_match.group(2)) if full_match.group(2) else 0
            time_str = f"{h}h {m}m"
        else:
            continue
    
    # Check charges and add charge time
    charges_match = re.search(r'<div class="stat-value">(\d+)</div><div class="stat-label">Stops', html)
    charges = int(charges_match.group(1)) if charges_match else 0
    
    if charges > 0:
        # Parse time_str back and add 30 min per charge
        tm = re.match(r'(\d+)h (\d+)m', time_str)
        if tm:
            h = int(tm.group(1))
            m = int(tm.group(2)) + (charges * 30)
            h += m // 60
            m = m % 60
            time_str = f"{h}h {m}m"
    
    # Replace total time in hero stats
    html = re.sub(
        r'<div class="stat-value">\d+h \d+m</div><div class="stat-label">Total',
        f'<div class="stat-value">{time_str}</div><div class="stat-label">Total',
        html
    )
    
    # Replace total trip in details
    html = re.sub(
        r'<span>Total Trip</span><span>\d+h \d+m</span>',
        f'<span>Total Trip</span><span>{time_str}</span>',
        html
    )
    
    # Replace in FAQ text
    html = re.sub(
        r'approximately \d+h \d+m',
        f'approximately {time_str}',
        html
    )
    html = re.sub(
        r'approximately <strong>\d+h \d+m</strong>',
        f'approximately <strong>{time_str}</strong>',
        html
    )
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Fixed {count} EV pages with actual drive times")
