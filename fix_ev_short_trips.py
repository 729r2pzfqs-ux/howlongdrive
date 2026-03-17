import os
import re

count = 0

for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find miles
    miles_match = re.search(r'<div class="stat-value">(\d+)</div><div class="stat-label">Miles', html)
    if not miles_match:
        continue
    miles = int(miles_match.group(1))
    
    # For short trips (under 50 miles), the time should be in minutes not hours
    if miles < 50:
        # Recalculate: ~1 min per mile
        drive_mins = max(5, int(miles * 1.3))  # ~1.3 min per mile average
        
        if drive_mins < 60:
            time_str = f"0h {drive_mins}m"
        else:
            h = drive_mins // 60
            m = drive_mins % 60
            time_str = f"{h}h {m}m"
        
        # Check if total time looks wrong (hours when should be minutes)
        if re.search(r'<div class="stat-value">\d{1,2}h 0m</div><div class="stat-label">Total', html):
            html = re.sub(
                r'<div class="stat-value">\d+h \d+m</div><div class="stat-label">Total',
                f'<div class="stat-value">{time_str}</div><div class="stat-label">Total',
                html
            )
            html = re.sub(
                r'<span>Total Trip</span><span>\d+h \d+m</span>',
                f'<span>Total Trip</span><span>{time_str}</span>',
                html
            )
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

print(f"✅ Fixed {count} short trip EV pages")
