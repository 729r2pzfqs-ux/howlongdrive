import os
import json
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 3959
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

# Regional city data
REGIONS = {
    "california": {
        "los-angeles": (34.0522, -118.2437, "Los Angeles"),
        "san-francisco": (37.7749, -122.4194, "San Francisco"),
        "san-diego": (32.7157, -117.1611, "San Diego"),
        "san-jose": (37.3382, -121.8863, "San Jose"),
        "fresno": (36.7378, -119.7871, "Fresno"),
        "oakland": (37.8044, -122.2712, "Oakland"),
        "long-beach": (33.7701, -118.1937, "Long Beach"),
        "bakersfield": (35.3733, -119.0187, "Bakersfield"),
        "anaheim": (33.8366, -117.9143, "Anaheim"),
        "santa-ana": (33.7455, -117.8677, "Santa Ana"),
        "riverside": (33.9533, -117.3962, "Riverside"),
        "stockton": (37.9577, -121.2908, "Stockton"),
        "irvine": (33.6846, -117.8265, "Irvine"),
        "santa-barbara": (34.4208, -119.6982, "Santa Barbara"),
        "palm-springs": (33.8303, -116.5453, "Palm Springs"),
        "pasadena": (34.1478, -118.1445, "Pasadena"),
        "santa-monica": (34.0195, -118.4912, "Santa Monica"),
        "berkeley": (37.8716, -122.2727, "Berkeley"),
        "palo-alto": (37.4419, -122.1430, "Palo Alto"),
        "sacramento": (38.5816, -121.4944, "Sacramento"),
    },
    "texas": {
        "houston": (29.7604, -95.3698, "Houston"),
        "dallas": (32.7767, -96.7970, "Dallas"),
        "austin": (30.2672, -97.7431, "Austin"),
        "san-antonio": (29.4241, -98.4936, "San Antonio"),
        "fort-worth": (32.7555, -97.3308, "Fort Worth"),
        "el-paso": (31.7619, -106.4850, "El Paso"),
        "arlington": (32.7357, -97.1081, "Arlington"),
        "corpus-christi": (27.8006, -97.3964, "Corpus Christi"),
        "plano": (33.0198, -96.6989, "Plano"),
        "lubbock": (33.5779, -101.8552, "Lubbock"),
        "laredo": (27.5306, -99.4803, "Laredo"),
        "irving": (32.8140, -96.9489, "Irving"),
        "amarillo": (35.2220, -101.8313, "Amarillo"),
        "galveston": (29.3013, -94.7977, "Galveston"),
        "mcallen": (26.2034, -98.2300, "McAllen"),
        "waco": (31.5493, -97.1467, "Waco"),
        "college-station": (30.6280, -96.3344, "College Station"),
        "round-rock": (30.5083, -97.6789, "Round Rock"),
        "the-woodlands": (30.1658, -95.4613, "The Woodlands"),
        "sugar-land": (29.6197, -95.6349, "Sugar Land"),
    },
    "florida": {
        "miami": (25.7617, -80.1918, "Miami"),
        "orlando": (28.5383, -81.3792, "Orlando"),
        "tampa": (27.9506, -82.4572, "Tampa"),
        "jacksonville": (30.3322, -81.6557, "Jacksonville"),
        "fort-lauderdale": (26.1224, -80.1373, "Fort Lauderdale"),
        "west-palm-beach": (26.7153, -80.0534, "West Palm Beach"),
        "st-petersburg": (27.7676, -82.6403, "St. Petersburg"),
        "clearwater": (27.9659, -82.8001, "Clearwater"),
        "naples": (26.1420, -81.7948, "Naples"),
        "sarasota": (27.3364, -82.5307, "Sarasota"),
        "fort-myers": (26.6406, -81.8723, "Fort Myers"),
        "gainesville": (29.6516, -82.3248, "Gainesville"),
        "tallahassee": (30.4383, -84.2807, "Tallahassee"),
        "pensacola": (30.4213, -87.2169, "Pensacola"),
        "daytona-beach": (29.2108, -81.0228, "Daytona Beach"),
        "key-west": (24.5551, -81.7800, "Key West"),
        "boca-raton": (26.3683, -80.1289, "Boca Raton"),
        "hollywood": (26.0112, -80.1495, "Hollywood"),
        "kissimmee": (28.2920, -81.4076, "Kissimmee"),
        "cape-coral": (26.5629, -81.9495, "Cape Coral"),
    },
    "northeast": {
        "new-york": (40.7128, -74.0060, "New York"),
        "boston": (42.3601, -71.0589, "Boston"),
        "philadelphia": (39.9526, -75.1652, "Philadelphia"),
        "washington-dc": (38.9072, -77.0369, "Washington DC"),
        "baltimore": (39.2904, -76.6122, "Baltimore"),
        "newark": (40.7357, -74.1724, "Newark"),
        "jersey-city": (40.7282, -74.0776, "Jersey City"),
        "providence": (41.8240, -71.4128, "Providence"),
        "hartford": (41.7658, -72.6734, "Hartford"),
        "new-haven": (41.3083, -72.9279, "New Haven"),
        "stamford": (41.0534, -73.5387, "Stamford"),
        "albany": (42.6526, -73.7562, "Albany"),
        "trenton": (40.2206, -74.7597, "Trenton"),
        "wilmington": (39.7391, -75.5398, "Wilmington"),
        "atlantic-city": (39.3643, -74.4229, "Atlantic City"),
        "princeton": (40.3573, -74.6672, "Princeton"),
        "annapolis": (38.9784, -76.4922, "Annapolis"),
        "cambridge": (42.3736, -71.1097, "Cambridge"),
        "worcester": (42.2626, -71.8023, "Worcester"),
        "springfield-ma": (42.1015, -72.5898, "Springfield MA"),
    }
}

routes = []
for region_name, cities in REGIONS.items():
    city_list = list(cities.items())
    for i, (from_slug, from_data) in enumerate(city_list):
        for j, (to_slug, to_data) in enumerate(city_list):
            if i >= j:
                continue
            
            dist_straight = haversine(from_data[0], from_data[1], to_data[0], to_data[1])
            dist = int(dist_straight * 1.3)
            hours = dist // 55
            mins = int((dist / 55 - hours) * 60)
            
            routes.append({
                "from_slug": from_slug,
                "from_name": from_data[2],
                "from_lat": from_data[0],
                "from_lon": from_data[1],
                "to_slug": to_slug,
                "to_name": to_data[2],
                "to_lat": to_data[0],
                "to_lon": to_data[1],
                "miles": dist,
                "hours": hours,
                "mins": mins,
                "region": region_name
            })
            # Add reverse route
            routes.append({
                "from_slug": to_slug,
                "from_name": to_data[2],
                "from_lat": to_data[0],
                "from_lon": to_data[1],
                "to_slug": from_slug,
                "to_name": from_data[2],
                "to_lat": from_data[0],
                "to_lon": from_data[1],
                "miles": dist,
                "hours": hours,
                "mins": mins,
                "region": region_name
            })

print(f"Generated {len(routes)} Phase 2 routes")
print(f"  California: {sum(1 for r in routes if r['region']=='california')}")
print(f"  Texas: {sum(1 for r in routes if r['region']=='texas')}")
print(f"  Florida: {sum(1 for r in routes if r['region']=='florida')}")
print(f"  Northeast: {sum(1 for r in routes if r['region']=='northeast')}")

with open("data/phase2_routes.json", "w") as f:
    json.dump(routes, f, indent=2)
