import os
import re

count = 0

for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}'):
        continue
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find drive time
    drive_match = re.search(r'<span>Drive Time</span><span>(\d+)h? ?(\d+)?m?i?n?</span>', html)
    if not drive_match:
        drive_match = re.search(r'<span>Drive Time</span><span>(\d+) min</span>', html)
        if drive_match:
            drive_mins = int(drive_match.group(1))
            drive_hours = 0
        else:
            continue
    else:
        drive_hours = int(drive_match.group(1)) if drive_match.group(1) else 0
        drive_mins = int(drive_match.group(2)) if drive_match.group(2) else 0
    
    # Check if total is 0h 0m
    if '0h 0m</div><div class="stat-label">Total' in html:
        # Calculate proper total (drive time + charge time)
        charges_match = re.search(r'<div class="stat-value">(\d+)</div><div class="stat-label">Stops', html)
        charges = int(charges_match.group(1)) if charges_match else 0
        
        total_mins = drive_mins + (charges * 30)  # 30 min per charge
        total_hours = drive_hours + (total_mins // 60)
        total_mins = total_mins % 60
        
        if total_hours == 0 and total_mins == 0:
            # Use drive time directly
            total_hours = drive_hours
            total_mins = drive_mins
        
        total_str = f"{total_hours}h {total_mins}m"
        
        # Replace all occurrences
        html = html.replace('0h 0m</div><div class="stat-label">Total', f'{total_str}</div><div class="stat-label">Total')
        html = re.sub(r'<span>Total Trip</span><span>0h 0m</span>', f'<span>Total Trip</span><span>{total_str}</span>', html)
        html = html.replace('approximately 0h 0m', f'approximately {total_str}')
        html = html.replace('approximately <strong>0h 0m</strong>', f'approximately <strong>{total_str}</strong>')
        
        with open(path, 'w') as f:
            f.write(html)
        count += 1

print(f"✅ Fixed total time on {count} EV pages")
