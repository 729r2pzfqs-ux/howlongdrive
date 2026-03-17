import os
import json
from math import radians, sin, cos, sqrt, atan2

# All 50 US State Capitals with coordinates
CAPITALS = {
    "montgomery-al": {"name": "Montgomery", "state": "AL", "lat": 32.3792, "lon": -86.3077},
    "juneau-ak": {"name": "Juneau", "state": "AK", "lat": 58.3019, "lon": -134.4197},
    "phoenix-az": {"name": "Phoenix", "state": "AZ", "lat": 33.4484, "lon": -112.0740},
    "little-rock-ar": {"name": "Little Rock", "state": "AR", "lat": 34.7465, "lon": -92.2896},
    "sacramento-ca": {"name": "Sacramento", "state": "CA", "lat": 38.5816, "lon": -121.4944},
    "denver-co": {"name": "Denver", "state": "CO", "lat": 39.7392, "lon": -104.9903},
    "hartford-ct": {"name": "Hartford", "state": "CT", "lat": 41.7658, "lon": -72.6734},
    "dover-de": {"name": "Dover", "state": "DE", "lat": 39.1582, "lon": -75.5244},
    "tallahassee-fl": {"name": "Tallahassee", "state": "FL", "lat": 30.4383, "lon": -84.2807},
    "atlanta-ga": {"name": "Atlanta", "state": "GA", "lat": 33.7490, "lon": -84.3880},
    "honolulu-hi": {"name": "Honolulu", "state": "HI", "lat": 21.3069, "lon": -157.8583},
    "boise-id": {"name": "Boise", "state": "ID", "lat": 43.6150, "lon": -116.2023},
    "springfield-il": {"name": "Springfield", "state": "IL", "lat": 39.7817, "lon": -89.6501},
    "indianapolis-in": {"name": "Indianapolis", "state": "IN", "lat": 39.7684, "lon": -86.1581},
    "des-moines-ia": {"name": "Des Moines", "state": "IA", "lat": 41.5868, "lon": -93.6250},
    "topeka-ks": {"name": "Topeka", "state": "KS", "lat": 39.0473, "lon": -95.6752},
    "frankfort-ky": {"name": "Frankfort", "state": "KY", "lat": 38.2009, "lon": -84.8733},
    "baton-rouge-la": {"name": "Baton Rouge", "state": "LA", "lat": 30.4515, "lon": -91.1871},
    "augusta-me": {"name": "Augusta", "state": "ME", "lat": 44.3106, "lon": -69.7795},
    "annapolis-md": {"name": "Annapolis", "state": "MD", "lat": 38.9784, "lon": -76.4922},
    "boston-ma": {"name": "Boston", "state": "MA", "lat": 42.3601, "lon": -71.0589},
    "lansing-mi": {"name": "Lansing", "state": "MI", "lat": 42.7325, "lon": -84.5555},
    "saint-paul-mn": {"name": "Saint Paul", "state": "MN", "lat": 44.9537, "lon": -93.0900},
    "jackson-ms": {"name": "Jackson", "state": "MS", "lat": 32.2988, "lon": -90.1848},
    "jefferson-city-mo": {"name": "Jefferson City", "state": "MO", "lat": 38.5767, "lon": -92.1735},
    "helena-mt": {"name": "Helena", "state": "MT", "lat": 46.5891, "lon": -112.0391},
    "lincoln-ne": {"name": "Lincoln", "state": "NE", "lat": 40.8258, "lon": -96.6852},
    "carson-city-nv": {"name": "Carson City", "state": "NV", "lat": 39.1638, "lon": -119.7674},
    "concord-nh": {"name": "Concord", "state": "NH", "lat": 43.2081, "lon": -71.5376},
    "trenton-nj": {"name": "Trenton", "state": "NJ", "lat": 40.2206, "lon": -74.7597},
    "santa-fe-nm": {"name": "Santa Fe", "state": "NM", "lat": 35.6870, "lon": -105.9378},
    "albany-ny": {"name": "Albany", "state": "NY", "lat": 42.6526, "lon": -73.7562},
    "raleigh-nc": {"name": "Raleigh", "state": "NC", "lat": 35.7796, "lon": -78.6382},
    "bismarck-nd": {"name": "Bismarck", "state": "ND", "lat": 46.8083, "lon": -100.7837},
    "columbus-oh": {"name": "Columbus", "state": "OH", "lat": 39.9612, "lon": -82.9988},
    "oklahoma-city-ok": {"name": "Oklahoma City", "state": "OK", "lat": 35.4676, "lon": -97.5164},
    "salem-or": {"name": "Salem", "state": "OR", "lat": 44.9429, "lon": -123.0351},
    "harrisburg-pa": {"name": "Harrisburg", "state": "PA", "lat": 40.2732, "lon": -76.8867},
    "providence-ri": {"name": "Providence", "state": "RI", "lat": 41.8240, "lon": -71.4128},
    "columbia-sc": {"name": "Columbia", "state": "SC", "lat": 34.0007, "lon": -81.0348},
    "pierre-sd": {"name": "Pierre", "state": "SD", "lat": 44.3683, "lon": -100.3510},
    "nashville-tn": {"name": "Nashville", "state": "TN", "lat": 36.1627, "lon": -86.7816},
    "austin-tx": {"name": "Austin", "state": "TX", "lat": 30.2672, "lon": -97.7431},
    "salt-lake-city-ut": {"name": "Salt Lake City", "state": "UT", "lat": 40.7608, "lon": -111.8910},
    "montpelier-vt": {"name": "Montpelier", "state": "VT", "lat": 44.2601, "lon": -72.5754},
    "richmond-va": {"name": "Richmond", "state": "VA", "lat": 37.5407, "lon": -77.4360},
    "olympia-wa": {"name": "Olympia", "state": "WA", "lat": 47.0379, "lon": -122.9007},
    "charleston-wv": {"name": "Charleston", "state": "WV", "lat": 38.3498, "lon": -81.6326},
    "madison-wi": {"name": "Madison", "state": "WI", "lat": 43.0731, "lon": -89.4012},
    "cheyenne-wy": {"name": "Cheyenne", "state": "WY", "lat": 41.1400, "lon": -104.8202}
}

def haversine(lat1, lon1, lat2, lon2):
    R = 3959  # Earth radius in miles
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def driving_distance(straight_line):
    return int(straight_line * 1.3)  # Roads are ~30% longer than straight line

def driving_time(miles):
    avg_speed = 55  # mph average including stops
    hours = miles / avg_speed
    h = int(hours)
    m = int((hours - h) * 60)
    return h, m

# Skip Honolulu (can't drive there)
skip = ["honolulu-hi"]

routes = []
for from_slug, from_data in CAPITALS.items():
    if from_slug in skip:
        continue
    for to_slug, to_data in CAPITALS.items():
        if to_slug in skip or from_slug == to_slug:
            continue
        
        dist_straight = haversine(from_data["lat"], from_data["lon"], to_data["lat"], to_data["lon"])
        dist = driving_distance(dist_straight)
        hours, mins = driving_time(dist)
        
        routes.append({
            "from_slug": from_slug,
            "from_name": f"{from_data['name']}, {from_data['state']}",
            "from_lat": from_data["lat"],
            "from_lon": from_data["lon"],
            "to_slug": to_slug,
            "to_name": f"{to_data['name']}, {to_data['state']}",
            "to_lat": to_data["lat"],
            "to_lon": to_data["lon"],
            "miles": dist,
            "hours": hours,
            "mins": mins
        })

print(f"Generated {len(routes)} capital routes (excluding Hawaii)")

# Save for reference
with open("data/capitals_routes.json", "w") as f:
    json.dump(routes, f, indent=2)
