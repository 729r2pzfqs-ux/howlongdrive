import os
import json
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 3959
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

# Phase 3 destinations
DESTINATIONS = {
    # National Parks
    "yellowstone": (44.4280, -110.5885, "Yellowstone National Park"),
    "yosemite": (37.8651, -119.5383, "Yosemite National Park"),
    "grand-canyon": (36.0544, -112.1401, "Grand Canyon"),
    "zion": (37.2982, -113.0263, "Zion National Park"),
    "glacier": (48.7596, -113.7870, "Glacier National Park"),
    "rocky-mountain": (40.3428, -105.6836, "Rocky Mountain NP"),
    "joshua-tree": (33.8734, -115.9010, "Joshua Tree"),
    "death-valley": (36.5054, -117.0794, "Death Valley"),
    "sequoia": (36.4864, -118.5658, "Sequoia National Park"),
    "arches": (38.7331, -109.5925, "Arches National Park"),
    "bryce-canyon": (37.5930, -112.1871, "Bryce Canyon"),
    "acadia": (44.3386, -68.2733, "Acadia National Park"),
    "everglades": (25.2866, -80.8987, "Everglades"),
    "big-bend": (29.2500, -103.2500, "Big Bend"),
    "great-smoky": (35.6118, -83.4895, "Great Smoky Mountains"),
    
    # College Towns
    "ann-arbor": (42.2808, -83.7430, "Ann Arbor"),
    "chapel-hill": (35.9132, -79.0558, "Chapel Hill"),
    "boulder": (40.0150, -105.2705, "Boulder"),
    "austin-ut": (30.2849, -97.7341, "Austin (UT)"),
    "madison-wi": (43.0731, -89.4012, "Madison"),
    "berkeley-ca": (37.8716, -122.2727, "Berkeley"),
    "columbus-osu": (39.9612, -82.9988, "Columbus"),
    "tucson": (32.2226, -110.9747, "Tucson"),
    "state-college": (40.7934, -77.8600, "State College"),
    "eugene": (44.0521, -123.0868, "Eugene"),
    "bloomington-in": (39.1653, -86.5264, "Bloomington IN"),
    "gainesville-fl": (29.6516, -82.3248, "Gainesville"),
    "norman": (35.2226, -97.4395, "Norman"),
    "college-station-tx": (30.6280, -96.3344, "College Station"),
    "ames": (42.0308, -93.6319, "Ames"),
    
    # Tourist Destinations
    "las-vegas": (36.1699, -115.1398, "Las Vegas"),
    "disneyland": (33.8121, -117.9190, "Disneyland"),
    "disney-world": (28.3852, -81.5639, "Disney World"),
    "myrtle-beach": (33.6891, -78.8867, "Myrtle Beach"),
    "virginia-beach": (36.8529, -75.9780, "Virginia Beach"),
    "napa-valley": (38.2975, -122.2869, "Napa Valley"),
    "lake-tahoe": (39.0968, -120.0324, "Lake Tahoe"),
    "aspen": (39.1911, -106.8175, "Aspen"),
    "sedona": (34.8697, -111.7610, "Sedona"),
    "new-orleans": (29.9511, -90.0715, "New Orleans"),
    "savannah": (32.0809, -81.0912, "Savannah"),
    "charleston-sc": (32.7765, -79.9311, "Charleston SC"),
    "san-juan": (18.4655, -66.1057, "San Juan"),
    "honolulu": (21.3069, -157.8583, "Honolulu"),  # Skip - can't drive
    "maui": (20.7984, -156.3319, "Maui"),  # Skip - can't drive
    "outer-banks": (35.5585, -75.4665, "Outer Banks"),
    "gatlinburg": (35.7143, -83.5102, "Gatlinburg"),
    "branson": (36.6437, -93.2185, "Branson"),
    "niagara-falls": (43.0896, -79.0849, "Niagara Falls"),
    "mount-rushmore": (43.8791, -103.4591, "Mount Rushmore"),
}

# Major cities to connect to destinations
MAJOR_CITIES = {
    "new-york": (40.7128, -74.0060, "New York"),
    "los-angeles": (34.0522, -118.2437, "Los Angeles"),
    "chicago": (41.8781, -87.6298, "Chicago"),
    "houston": (29.7604, -95.3698, "Houston"),
    "phoenix": (33.4484, -112.0740, "Phoenix"),
    "philadelphia": (39.9526, -75.1652, "Philadelphia"),
    "san-antonio": (29.4241, -98.4936, "San Antonio"),
    "san-diego": (32.7157, -117.1611, "San Diego"),
    "dallas": (32.7767, -96.7970, "Dallas"),
    "san-jose": (37.3382, -121.8863, "San Jose"),
    "austin": (30.2672, -97.7431, "Austin"),
    "jacksonville": (30.3322, -81.6557, "Jacksonville"),
    "san-francisco": (37.7749, -122.4194, "San Francisco"),
    "seattle": (47.6062, -122.3321, "Seattle"),
    "denver": (39.7392, -104.9903, "Denver"),
    "boston": (42.3601, -71.0589, "Boston"),
    "atlanta": (33.7490, -84.3880, "Atlanta"),
    "miami": (25.7617, -80.1918, "Miami"),
    "minneapolis": (44.9778, -93.2650, "Minneapolis"),
    "portland": (45.5152, -122.6784, "Portland"),
}

# Skip Hawaii destinations
skip_destinations = ["honolulu", "maui", "san-juan"]

routes = []
for dest_slug, dest_data in DESTINATIONS.items():
    if dest_slug in skip_destinations:
        continue
    for city_slug, city_data in MAJOR_CITIES.items():
        dist_straight = haversine(dest_data[0], dest_data[1], city_data[0], city_data[1])
        dist = int(dist_straight * 1.3)
        hours = dist // 55
        mins = int((dist / 55 - hours) * 60)
        
        # Both directions
        routes.append({
            "from_slug": city_slug, "from_name": city_data[2],
            "from_lat": city_data[0], "from_lon": city_data[1],
            "to_slug": dest_slug, "to_name": dest_data[2],
            "to_lat": dest_data[0], "to_lon": dest_data[1],
            "miles": dist, "hours": hours, "mins": mins
        })
        routes.append({
            "from_slug": dest_slug, "from_name": dest_data[2],
            "from_lat": dest_data[0], "from_lon": dest_data[1],
            "to_slug": city_slug, "to_name": city_data[2],
            "to_lat": city_data[0], "to_lon": city_data[1],
            "miles": dist, "hours": hours, "mins": mins
        })

print(f"Generated {len(routes)} Phase 3 routes")
print(f"  National Parks: ~300 routes")
print(f"  College Towns: ~300 routes")
print(f"  Tourist Destinations: ~400 routes")

with open("data/phase3_routes.json", "w") as f:
    json.dump(routes, f)
