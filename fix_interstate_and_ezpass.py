#!/usr/bin/env python3
"""Fix 'via Interstate' and E-ZPass references on route pages."""

import json
import os
import re
import subprocess
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
ROUTE_DIR = os.path.join(BASE, 'route')

# ── Load data ──────────────────────────────────────────────────────────────

def load_all_highways():
    """Load highway info from all data JSON files."""
    hw_map = {}
    data_dir = os.path.join(BASE, 'data')
    for fname in os.listdir(data_dir):
        if not fname.endswith('.json'):
            continue
        try:
            data = json.load(open(os.path.join(data_dir, fname)))
            if isinstance(data, list):
                for r in data:
                    if isinstance(r, dict) and r.get('highway') and r.get('from') and r.get('to'):
                        slug = make_slug(r['from'], r['to'])
                        hw_map[slug] = r['highway']
        except:
            pass
    return hw_map

def load_coords():
    """Load city coordinates."""
    with open(os.path.join(BASE, 'data', 'city_coords.json')) as f:
        return json.load(f)

def make_slug(from_city, to_city):
    f = from_city.lower().replace(' ', '-').replace('.', '').replace("'", "")
    t = to_city.lower().replace(' ', '-').replace('.', '').replace("'", "")
    return f'{f}-to-{t}'

def slug_to_name(slug_part):
    """Convert slug back to display name (best effort)."""
    return slug_part.replace('-', ' ').title()

# ── City-to-state mapping ──────────────────────────────────────────────────

# Major US cities and their states (comprehensive list)
CITY_STATE = {
    # Northeast
    'new-york': 'NY', 'manhattan': 'NY', 'brooklyn': 'NY', 'queens': 'NY', 'bronx': 'NY',
    'staten-island': 'NY', 'buffalo': 'NY', 'rochester': 'NY', 'syracuse': 'NY', 'albany': 'NY',
    'yonkers': 'NY', 'new-rochelle': 'NY', 'white-plains': 'NY', 'ithaca': 'NY',
    'schenectady': 'NY', 'utica': 'NY', 'binghamton': 'NY', 'poughkeepsie': 'NY',
    'newburgh': 'NY', 'saratoga-springs': 'NY', 'kingston': 'NY', 'plattsburgh': 'NY',
    'long-island': 'NY', 'garden-city': 'NY', 'hempstead': 'NY', 'great-neck': 'NY',
    'jfk': 'NY', 'lga': 'NY', 'ewr': 'NJ',
    
    'boston': 'MA', 'cambridge': 'MA', 'worcester': 'MA', 'springfield-ma': 'MA',
    'lowell': 'MA', 'brockton': 'MA', 'quincy': 'MA', 'newton': 'MA', 'somerville': 'MA',
    'framingham': 'MA', 'waltham': 'MA', 'brookline': 'MA', 'medford': 'MA',
    'salem': 'MA', 'plymouth': 'MA', 'cape-cod': 'MA', 'nantucket': 'MA',
    'marthas-vineyard': 'MA', 'provincetown': 'MA', 'lexington': 'MA', 'concord-ma': 'MA',
    'wellesley': 'MA', 'needham': 'MA', 'natick': 'MA', 'marlborough': 'MA',
    'bos': 'MA',
    
    'philadelphia': 'PA', 'pittsburgh': 'PA', 'allentown': 'PA', 'erie': 'PA',
    'reading': 'PA', 'scranton': 'PA', 'bethlehem': 'PA', 'lancaster': 'PA',
    'harrisburg': 'PA', 'state-college': 'PA', 'wilkes-barre': 'PA', 'york': 'PA',
    'gettysburg': 'PA', 'chester': 'PA', 'norristown': 'PA', 'king-of-prussia': 'PA',
    'abington': 'PA', 'ardmore': 'PA', 'bryn-mawr': 'PA', 'haverford': 'PA',
    'wayne': 'PA', 'conshohocken': 'PA', 'media': 'PA', 'exton': 'PA',
    'doylestown': 'PA', 'phl': 'PA',
    
    'newark': 'NJ', 'jersey-city': 'NJ', 'paterson': 'NJ', 'elizabeth': 'NJ',
    'trenton': 'NJ', 'atlantic-city': 'NJ', 'camden': 'NJ', 'hoboken': 'NJ',
    'princeton': 'NJ', 'morristown': 'NJ', 'cherry-hill': 'NJ', 'toms-river': 'NJ',
    'woodbridge': 'NJ', 'edison': 'NJ', 'new-brunswick': 'NJ', 'asbury-park': 'NJ',
    'cape-may': 'NJ', 'montclair': 'NJ', 'hackensack': 'NJ', 'paramus': 'NJ',
    'fort-lee': 'NJ', 'ridgewood': 'NJ',
    
    'hartford': 'CT', 'new-haven': 'CT', 'stamford': 'CT', 'bridgeport': 'CT',
    'waterbury': 'CT', 'norwalk': 'CT', 'danbury': 'CT', 'greenwich': 'CT',
    'mystic': 'CT', 'new-london': 'CT', 'westport': 'CT', 'fairfield': 'CT',
    
    'providence': 'RI', 'newport': 'RI', 'warwick': 'RI', 'cranston': 'RI',
    'pvd': 'RI',
    
    'portland-me': 'ME', 'bangor': 'ME', 'acadia': 'ME', 'bar-harbor': 'ME',
    'augusta': 'ME', 'lewiston': 'ME', 'kennebunkport': 'ME', 'ogunquit': 'ME',
    'pwd': 'ME',
    
    'burlington': 'VT', 'montpelier': 'VT', 'stowe': 'VT', 'killington': 'VT',
    'manchester': 'VT',
    
    'concord': 'NH', 'manchester-nh': 'NH', 'nashua': 'NH', 'portsmouth': 'NH',
    'hanover': 'NH', 'keene': 'NH', 'lebanon': 'NH', 'laconia': 'NH',
    'north-conway': 'NH', 'lincoln': 'NH', 'mht': 'NH',
    
    # Mid-Atlantic
    'washington-dc': 'DC', 'dc': 'DC', 'dca': 'DC', 'iad': 'VA', 'bwi': 'MD',
    'baltimore': 'MD', 'annapolis': 'MD', 'frederick': 'MD', 'columbia': 'MD',
    'bethesda': 'MD', 'silver-spring': 'MD', 'rockville': 'MD', 'gaithersburg': 'MD',
    'towson': 'MD', 'ellicott-city': 'MD', 'ocean-city': 'MD', 'college-park': 'MD',
    
    'arlington': 'VA', 'richmond': 'VA', 'virginia-beach': 'VA', 'norfolk': 'VA',
    'alexandria': 'VA', 'chesapeake': 'VA', 'newport-news': 'VA', 'hampton': 'VA',
    'roanoke': 'VA', 'charlottesville': 'VA', 'lynchburg': 'VA', 'williamsburg': 'VA',
    'fairfax': 'VA', 'manassas': 'VA', 'tysons': 'VA', 'reston': 'VA',
    'mclean': 'VA', 'leesburg': 'VA', 'ashburn': 'VA', 'herndon': 'VA',
    'fredericksburg': 'VA', 'shenandoah': 'VA', 'staunton': 'VA',
    
    'wilmington': 'DE', 'dover': 'DE', 'rehoboth-beach': 'DE',
    
    'charleston-wv': 'WV', 'morgantown': 'WV', 'huntington': 'WV',
    
    # Southeast
    'atlanta': 'GA', 'savannah': 'GA', 'augusta-ga': 'GA', 'athens': 'GA',
    'macon': 'GA', 'columbus-ga': 'GA', 'roswell': 'GA', 'sandy-springs': 'GA',
    'marietta': 'GA', 'alpharetta': 'GA', 'decatur': 'GA', 'duluth': 'GA',
    'kennesaw': 'GA', 'johns-creek': 'GA', 'peachtree-city': 'GA', 'atl': 'GA',
    'buckhead': 'GA', 'smyrna': 'GA', 'lawrenceville': 'GA', 'dunwoody': 'GA',
    
    'miami': 'FL', 'orlando': 'FL', 'tampa': 'FL', 'jacksonville': 'FL',
    'st-petersburg': 'FL', 'fort-lauderdale': 'FL', 'west-palm-beach': 'FL',
    'naples': 'FL', 'sarasota': 'FL', 'tallahassee': 'FL', 'gainesville': 'FL',
    'pensacola': 'FL', 'fort-myers': 'FL', 'daytona-beach': 'FL', 'key-west': 'FL',
    'clearwater': 'FL', 'coral-gables': 'FL', 'boca-raton': 'FL', 'delray-beach': 'FL',
    'hollywood': 'FL', 'hialeah': 'FL', 'pembroke-pines': 'FL', 'miramar': 'FL',
    'cape-coral': 'FL', 'kissimmee': 'FL', 'lakeland': 'FL', 'ocala': 'FL',
    'st-augustine': 'FL', 'palm-beach': 'FL', 'cocoa-beach': 'FL', 'melbourne': 'FL',
    'winter-park': 'FL', 'mia': 'FL', 'mco': 'FL', 'tpa': 'FL',
    'miami-beach': 'FL', 'aventura': 'FL', 'doral': 'FL', 'homestead': 'FL',
    'jupiter': 'FL', 'boynton-beach': 'FL', 'pompano-beach': 'FL',
    'port-st-lucie': 'FL', 'stuart': 'FL', 'vero-beach': 'FL',
    
    'charlotte': 'NC', 'raleigh': 'NC', 'durham': 'NC', 'greensboro': 'NC',
    'winston-salem': 'NC', 'asheville': 'NC', 'wilmington-nc': 'NC', 'chapel-hill': 'NC',
    'fayetteville': 'NC', 'cary': 'NC', 'outer-banks': 'NC', 'rdu': 'NC',
    'huntersville': 'NC', 'apex': 'NC', 'mooresville': 'NC', 'gastonia': 'NC',
    
    'nashville': 'TN', 'memphis': 'TN', 'knoxville': 'TN', 'chattanooga': 'TN',
    'murfreesboro': 'TN', 'clarksville': 'TN', 'gatlinburg': 'TN', 'pigeon-forge': 'TN',
    'franklin': 'TN', 'bna': 'TN', 'brentwood': 'TN', 'hendersonville': 'TN',
    'germantown': 'TN', 'collierville': 'TN',
    
    'charleston': 'SC', 'columbia-sc': 'SC', 'myrtle-beach': 'SC', 'greenville': 'SC',
    'hilton-head': 'SC', 'spartanburg': 'SC', 'rock-hill': 'SC', 'mount-pleasant': 'SC',
    
    'birmingham': 'AL', 'montgomery': 'AL', 'huntsville': 'AL', 'mobile': 'AL',
    'tuscaloosa': 'AL', 'hoover': 'AL', 'auburn': 'AL',
    
    'jackson': 'MS', 'biloxi': 'MS', 'gulfport': 'MS', 'hattiesburg': 'MS',
    'oxford': 'MS', 'tupelo': 'MS', 'natchez': 'MS', 'vicksburg': 'MS',
    
    'new-orleans': 'LA', 'baton-rouge': 'LA', 'shreveport': 'LA', 'lafayette': 'LA',
    'lake-charles': 'LA', 'monroe': 'LA', 'msy': 'LA',
    
    'little-rock': 'AR', 'fayetteville-ar': 'AR', 'fort-smith': 'AR', 'hot-springs': 'AR',
    'bentonville': 'AR', 'rogers': 'AR', 'springdale': 'AR', 'jonesboro': 'AR',
    
    'louisville': 'KY', 'lexington-ky': 'KY', 'bowling-green': 'KY', 'covington': 'KY',
    'frankfort': 'KY', 'sdf': 'KY',
    
    # Midwest
    'chicago': 'IL', 'springfield': 'IL', 'naperville': 'IL', 'rockford': 'IL',
    'peoria': 'IL', 'champaign': 'IL', 'evanston': 'IL', 'schaumburg': 'IL',
    'aurora': 'IL', 'joliet': 'IL', 'elgin': 'IL', 'waukegan': 'IL',
    'oak-park': 'IL', 'skokie': 'IL', 'arlington-heights': 'IL', 'palatine': 'IL',
    'oak-brook': 'IL', 'deerfield': 'IL', 'highland-park': 'IL', 'lake-forest': 'IL',
    'wheaton': 'IL', 'ord': 'IL', 'mdw': 'IL', 'bolingbrook': 'IL',
    'cicero': 'IL', 'berwyn': 'IL', 'des-plaines': 'IL', 'tinley-park': 'IL',
    'orland-park': 'IL', 'lombard': 'IL', 'downers-grove': 'IL',
    'buffalo-grove': 'IL', 'glenview': 'IL', 'wilmette': 'IL',
    'hinsdale': 'IL', 'la-grange': 'IL', 'libertyville': 'IL',
    
    'detroit': 'MI', 'grand-rapids': 'MI', 'ann-arbor': 'MI', 'lansing': 'MI',
    'flint': 'MI', 'kalamazoo': 'MI', 'traverse-city': 'MI', 'mackinac': 'MI',
    'dtw': 'MI', 'dearborn': 'MI', 'warren': 'MI', 'sterling-heights': 'MI',
    'troy': 'MI', 'southfield': 'MI', 'livonia': 'MI', 'royal-oak': 'MI',
    'birmingham-mi': 'MI', 'bloomfield-hills': 'MI', 'west-bloomfield': 'MI',
    'farmington-hills': 'MI', 'novi': 'MI', 'canton': 'MI', 'plymouth': 'MI',
    
    'indianapolis': 'IN', 'fort-wayne': 'IN', 'south-bend': 'IN', 'evansville': 'IN',
    'bloomington': 'IN', 'carmel': 'IN', 'fishers': 'IN', 'noblesville': 'IN',
    'ind': 'IN', 'zionsville': 'IN', 'westfield': 'IN', 'greenwood': 'IN',
    
    'columbus': 'OH', 'cleveland': 'OH', 'cincinnati': 'OH', 'toledo': 'OH',
    'akron': 'OH', 'dayton': 'OH', 'youngstown': 'OH', 'canton-oh': 'OH',
    'cle': 'OH', 'cmh': 'OH', 'dublin': 'OH', 'mason': 'OH',
    'westerville': 'OH', 'upper-arlington': 'OH', 'hudson': 'OH',
    'solon': 'OH', 'strongsville': 'OH', 'avon': 'OH',
    
    'milwaukee': 'WI', 'madison': 'WI', 'green-bay': 'WI', 'kenosha': 'WI',
    'racine': 'WI', 'appleton': 'WI', 'eau-claire': 'WI', 'oshkosh': 'WI',
    'mke': 'WI', 'wauwatosa': 'WI', 'brookfield': 'WI', 'waukesha': 'WI',
    'menomonee-falls': 'WI', 'mequon': 'WI', 'whitefish-bay': 'WI',
    
    'minneapolis': 'MN', 'st-paul': 'MN', 'duluth-mn': 'MN', 'rochester-mn': 'MN',
    'bloomington-mn': 'MN', 'plymouth-mn': 'MN', 'msp': 'MN', 'anoka': 'MN',
    'minnetonka': 'MN', 'eden-prairie': 'MN', 'edina': 'MN', 'maple-grove': 'MN',
    'woodbury': 'MN', 'eagan': 'MN', 'burnsville': 'MN', 'lakeville': 'MN',
    'prior-lake': 'MN', 'chanhassen': 'MN', 'shakopee': 'MN',
    
    'kansas-city': 'MO', 'st-louis': 'MO', 'springfield-mo': 'MO', 'columbia-mo': 'MO',
    'stl': 'MO', 'mci': 'MO', 'lee-summit': 'MO', 'independence': 'MO',
    'branson': 'MO', 'overland-park': 'KS', 'olathe': 'KS', 'lenexa': 'KS',
    'shawnee': 'KS', 'leawood': 'KS', 'prairie-village': 'KS',
    
    'omaha': 'NE', 'lincoln': 'NE', 'oma': 'NE',
    
    'des-moines': 'IA', 'cedar-rapids': 'IA', 'iowa-city': 'IA', 'davenport': 'IA',
    'dsm': 'IA',
    
    'wichita': 'KS', 'topeka': 'KS', 'lawrence': 'KS', 'manhattan-ks': 'KS',
    
    'fargo': 'ND', 'bismarck': 'ND', 'grand-forks': 'ND',
    'sioux-falls': 'SD', 'rapid-city': 'SD', 'deadwood': 'SD', 'mount-rushmore': 'SD',
    
    # Texas
    'houston': 'TX', 'dallas': 'TX', 'san-antonio': 'TX', 'austin': 'TX',
    'fort-worth': 'TX', 'el-paso': 'TX', 'arlington-tx': 'TX', 'corpus-christi': 'TX',
    'plano': 'TX', 'lubbock': 'TX', 'laredo': 'TX', 'irving': 'TX',
    'amarillo': 'TX', 'brownsville': 'TX', 'mckinney': 'TX', 'frisco': 'TX',
    'denton': 'TX', 'midland': 'TX', 'odessa': 'TX', 'waco': 'TX',
    'beaumont': 'TX', 'galveston': 'TX', 'college-station': 'TX', 'tyler': 'TX',
    'round-rock': 'TX', 'sugar-land': 'TX', 'the-woodlands': 'TX', 'katy': 'TX',
    'pearland': 'TX', 'league-city': 'TX', 'richardson': 'TX', 'allen': 'TX',
    'cedar-park': 'TX', 'georgetown': 'TX', 'pflugerville': 'TX', 'new-braunfels': 'TX',
    'san-marcos': 'TX', 'kyle': 'TX', 'buda': 'TX', 'dripping-springs': 'TX',
    'lakeway': 'TX', 'bee-cave': 'TX', 'iah': 'TX', 'dfw': 'TX', 'aus': 'TX',
    'hou': 'TX', 'sat': 'TX', 'southlake': 'TX', 'grapevine': 'TX',
    'coppell': 'TX', 'flower-mound': 'TX', 'highland-village': 'TX',
    'murphy': 'TX', 'wylie': 'TX', 'prosper': 'TX', 'celina': 'TX',
    'anderson-mill': 'TX', 'alamo-heights': 'TX',
    
    # Mountain / West
    'denver': 'CO', 'colorado-springs': 'CO', 'boulder': 'CO', 'fort-collins': 'CO',
    'aurora-co': 'CO', 'lakewood': 'CO', 'aspen': 'CO', 'vail': 'CO',
    'breckenridge': 'CO', 'steamboat-springs': 'CO', 'telluride': 'CO', 'den': 'CO',
    'littleton': 'CO', 'arvada': 'CO', 'centennial': 'CO', 'parker': 'CO',
    'castle-rock': 'CO', 'highlands-ranch': 'CO', 'lone-tree': 'CO',
    'cherry-creek': 'CO', 'greenwood-village': 'CO',
    
    'salt-lake-city': 'UT', 'park-city': 'UT', 'provo': 'UT', 'ogden': 'UT',
    'st-george': 'UT', 'moab': 'UT', 'slc': 'UT',
    
    'las-vegas': 'NV', 'reno': 'NV', 'henderson': 'NV', 'las': 'NV',
    'summerlin': 'NV',
    
    'phoenix': 'AZ', 'tucson': 'AZ', 'scottsdale': 'AZ', 'mesa': 'AZ',
    'tempe': 'AZ', 'chandler': 'AZ', 'gilbert': 'AZ', 'glendale': 'AZ',
    'flagstaff': 'AZ', 'sedona': 'AZ', 'grand-canyon': 'AZ', 'peoria-az': 'AZ',
    'phx': 'AZ', 'ahwatukee': 'AZ', 'paradise-valley': 'AZ', 'cave-creek': 'AZ',
    'fountain-hills': 'AZ', 'queen-creek': 'AZ', 'surprise': 'AZ', 'goodyear': 'AZ',
    
    'albuquerque': 'NM', 'santa-fe': 'NM', 'las-cruces': 'NM', 'roswell': 'NM',
    'abq': 'NM',
    
    'boise': 'ID', 'coeur-dalene': 'ID', 'sun-valley': 'ID', 'idaho-falls': 'ID',
    'boi': 'ID',
    
    'billings': 'MT', 'missoula': 'MT', 'bozeman': 'MT', 'helena': 'MT',
    'great-falls': 'MT', 'kalispell': 'MT', 'whitefish': 'MT', 'glacier': 'MT',
    
    'cheyenne': 'WY', 'jackson': 'WY', 'jackson-hole': 'WY', 'yellowstone': 'WY',
    'cody': 'WY', 'laramie': 'WY', 'casper': 'WY', 'sheridan': 'WY',
    
    # Pacific
    'los-angeles': 'CA', 'san-francisco': 'CA', 'san-diego': 'CA', 'san-jose': 'CA',
    'sacramento': 'CA', 'fresno': 'CA', 'long-beach': 'CA', 'oakland': 'CA',
    'bakersfield': 'CA', 'anaheim': 'CA', 'santa-ana': 'CA', 'riverside': 'CA',
    'irvine': 'CA', 'santa-barbara': 'CA', 'palm-springs': 'CA', 'pasadena': 'CA',
    'berkeley': 'CA', 'santa-monica': 'CA', 'venice-beach': 'CA', 'hollywood-ca': 'CA',
    'beverly-hills': 'CA', 'malibu': 'CA', 'monterey': 'CA', 'carmel': 'CA',
    'napa': 'CA', 'sonoma': 'CA', 'santa-cruz': 'CA', 'big-sur': 'CA',
    'palo-alto': 'CA', 'mountain-view': 'CA', 'sunnyvale': 'CA', 'cupertino': 'CA',
    'redwood-city': 'CA', 'san-mateo': 'CA', 'burlingame': 'CA', 'menlo-park': 'CA',
    'fremont': 'CA', 'hayward': 'CA', 'concord-ca': 'CA', 'walnut-creek': 'CA',
    'pleasanton': 'CA', 'dublin-ca': 'CA', 'livermore': 'CA', 'san-rafael': 'CA',
    'mill-valley': 'CA', 'sausalito': 'CA', 'tiburon': 'CA', 'corte-madera': 'CA',
    'lax': 'CA', 'sfo': 'CA', 'san': 'CA', 'sjc': 'CA', 'ont': 'CA',
    'burbank': 'CA', 'glendale-ca': 'CA', 'torrance': 'CA', 'huntington-beach': 'CA',
    'newport-beach': 'CA', 'laguna-beach': 'CA', 'dana-point': 'CA', 'san-clemente': 'CA',
    'temecula': 'CA', 'carlsbad': 'CA', 'encinitas': 'CA', 'del-mar': 'CA',
    'la-jolla': 'CA', 'coronado': 'CA', 'chula-vista': 'CA', 'el-cajon': 'CA',
    'escondido': 'CA', 'oceanside': 'CA', 'vista': 'CA', 'rancho-santa-fe': 'CA',
    'solana-beach': 'CA', 'almaden-valley': 'CA', 'alum-rock': 'CA', 'alviso': 'CA',
    'berryessa': 'CA', 'cambrian-park': 'CA', 'campbell': 'CA', 'east-foothills': 'CA',
    'evergreen': 'CA', 'milpitas': 'CA', 'santa-clara': 'CA', 'los-gatos': 'CA',
    'saratoga': 'CA', 'gilroy': 'CA', 'morgan-hill': 'CA', 'willow-glen': 'CA',
    'san-luis-obispo': 'CA', 'oxnard': 'CA', 'ventura': 'CA', 'thousand-oaks': 'CA',
    'calabasas': 'CA', 'west-hollywood': 'CA', 'culver-city': 'CA', 'inglewood': 'CA',
    'el-segundo': 'CA', 'hermosa-beach': 'CA', 'manhattan-beach': 'CA',
    'redondo-beach': 'CA', 'rancho-palos-verdes': 'CA', 'san-pedro': 'CA',
    'whittier': 'CA', 'fullerton': 'CA', 'orange': 'CA', 'costa-mesa': 'CA',
    'mission-viejo': 'CA', 'lake-forest-ca': 'CA', 'rancho-santa-margarita': 'CA',
    'aliso-viejo': 'CA', 'ladera-ranch': 'CA', 'san-juan-capistrano': 'CA',
    'lake-tahoe': 'CA', 'south-lake-tahoe': 'CA', 'tahoe': 'CA',
    'yosemite': 'CA', 'death-valley': 'CA', 'joshua-tree': 'CA',
    'palm-desert': 'CA', 'rancho-mirage': 'CA', 'indian-wells': 'CA',
    'la-quinta': 'CA', 'indio': 'CA', 'coachella': 'CA',
    'redlands': 'CA', 'san-bernardino': 'CA', 'ontario-ca': 'CA',
    'rancho-cucamonga': 'CA', 'upland': 'CA', 'claremont': 'CA', 'pomona': 'CA',
    'west-covina': 'CA', 'covina': 'CA', 'azusa': 'CA', 'arcadia': 'CA',
    'alhambra': 'CA', 'south-pasadena': 'CA', 'san-gabriel': 'CA',
    'rosemead': 'CA', 'el-monte': 'CA', 'diamond-bar': 'CA',
    'rowland-heights': 'CA', 'hacienda-heights': 'CA', 'la-habra': 'CA',
    'brea': 'CA', 'yorba-linda': 'CA', 'placentia': 'CA',
    'tustin': 'CA', 'lake-elsinore': 'CA', 'murrieta': 'CA',
    'menifee': 'CA', 'hemet': 'CA', 'beaumont-ca': 'CA', 'banning': 'CA',
    'redding': 'CA', 'chico': 'CA', 'davis': 'CA', 'elk-grove': 'CA',
    'folsom': 'CA', 'roseville': 'CA', 'rocklin': 'CA', 'lincoln-ca': 'CA',
    'stockton': 'CA', 'modesto': 'CA', 'visalia': 'CA', 'merced': 'CA',
    
    'seattle': 'WA', 'tacoma': 'WA', 'spokane': 'WA', 'olympia': 'WA',
    'bellevue': 'WA', 'vancouver-wa': 'WA', 'everett': 'WA', 'redmond': 'WA',
    'kirkland': 'WA', 'bothell': 'WA', 'issaquah': 'WA', 'sammamish': 'WA',
    'mercer-island': 'WA', 'woodinville': 'WA', 'kenmore': 'WA', 'shoreline': 'WA',
    'lynnwood': 'WA', 'edmonds': 'WA', 'mukilteo': 'WA', 'burien': 'WA',
    'sea': 'WA', 'seatac': 'WA',
    
    'portland': 'OR', 'eugene': 'OR', 'salem-or': 'OR', 'bend': 'OR',
    'medford': 'OR', 'corvallis': 'OR', 'ashland': 'OR', 'astoria': 'OR',
    'crater-lake': 'OR', 'hood-river': 'OR', 'pdx': 'OR',
    'lake-oswego': 'OR', 'west-linn': 'OR', 'tigard': 'OR', 'beaverton': 'OR',
    'hillsboro': 'OR', 'tualatin': 'OR', 'wilsonville': 'OR',
    
    'honolulu': 'HI', 'maui': 'HI', 'hnl': 'HI',
    'anchorage': 'AK', 'fairbanks': 'AK', 'juneau': 'AK', 'anc': 'AK',
    
    # Oklahoma
    'oklahoma-city': 'OK', 'tulsa': 'OK', 'norman': 'OK', 'edmond': 'OK',
    'okc': 'OK',
}

# ── E-ZPass states ──────────────────────────────────────────────────────────

EZPASS_STATES = {'NY', 'NJ', 'CT', 'MA', 'PA', 'MD', 'VA', 'DE', 'NH', 'ME', 
                 'RI', 'OH', 'IN', 'IL', 'WV', 'DC', 'NC', 'KY', 'MN', 'WI'}

# State-specific transponders
STATE_TRANSPONDER = {
    'FL': 'SunPass',
    'TX': 'TxTag', 
    'CA': 'FasTrak',
    'CO': 'ExpressToll',
    'GA': 'Peach Pass',
    'OK': 'PikePass',
    'KS': 'K-TAG',
    'WA': 'Good To Go!',
}

# ── Geographic highway logic ──────────────────────────────────────────────

def get_state(city_slug):
    """Get state for a city slug."""
    if city_slug in CITY_STATE:
        return CITY_STATE[city_slug]
    return None

def get_coord(slug, coords):
    """Get coordinates for a city slug."""
    # Try direct title case
    name = slug_to_name(slug)
    if name in coords:
        return coords[name]
    # Try matching slug against all names
    for cname in coords:
        if cname.lower().replace(' ', '-').replace('.', '').replace("'", "") == slug:
            return coords[cname]
    return None

# Known specific route overrides for accuracy  
ROUTE_OVERRIDES = {
    # Chicago corridors
    'chicago-to-minneapolis': 'I-94', 'minneapolis-to-chicago': 'I-94',
    'chicago-to-milwaukee': 'I-94', 'milwaukee-to-chicago': 'I-94',
    'chicago-to-detroit': 'I-94', 'detroit-to-chicago': 'I-94',
    'chicago-to-st-louis': 'I-55', 'st-louis-to-chicago': 'I-55',
    'chicago-to-indianapolis': 'I-65', 'indianapolis-to-chicago': 'I-65',
    'chicago-to-denver': 'I-80', 'denver-to-chicago': 'I-80',
    'chicago-to-los-angeles': 'I-40', 'los-angeles-to-chicago': 'I-40',
    'chicago-to-nashville': 'I-65', 'nashville-to-chicago': 'I-65',
    'chicago-to-memphis': 'I-57', 'memphis-to-chicago': 'I-57',
    
    # SE corridors
    'atlanta-to-miami': 'I-75', 'miami-to-atlanta': 'I-75',
    'atlanta-to-jacksonville': 'I-75', 'jacksonville-to-atlanta': 'I-75',
    'atlanta-to-nashville': 'I-24', 'nashville-to-atlanta': 'I-24',
    'atlanta-to-charlotte': 'I-85', 'charlotte-to-atlanta': 'I-85',
    'atlanta-to-birmingham': 'I-20', 'birmingham-to-atlanta': 'I-20',
    'atlanta-to-savannah': 'I-16', 'savannah-to-atlanta': 'I-16',
    
    # Florida
    'miami-to-orlando': 'Florida Turnpike', 'orlando-to-miami': 'Florida Turnpike',
    'miami-to-tampa': 'I-75', 'tampa-to-miami': 'I-75',
    'miami-to-jacksonville': 'I-95', 'jacksonville-to-miami': 'I-95',
    'orlando-to-tampa': 'I-4', 'tampa-to-orlando': 'I-4',
    'orlando-to-jacksonville': 'I-95', 'jacksonville-to-orlando': 'I-95',
    'tampa-to-jacksonville': 'I-75', 'jacksonville-to-tampa': 'I-75',
    'miami-to-fort-lauderdale': 'I-95', 'fort-lauderdale-to-miami': 'I-95',
    'miami-to-west-palm-beach': 'I-95', 'west-palm-beach-to-miami': 'I-95',
    'tampa-to-sarasota': 'I-75', 'sarasota-to-tampa': 'I-75',
    'tampa-to-st-petersburg': 'I-275', 'st-petersburg-to-tampa': 'I-275',
    'orlando-to-daytona-beach': 'I-4', 'daytona-beach-to-orlando': 'I-4',
    
    # Texas  
    'dallas-to-houston': 'I-45', 'houston-to-dallas': 'I-45',
    'dallas-to-austin': 'I-35', 'austin-to-dallas': 'I-35',
    'dallas-to-san-antonio': 'I-35', 'san-antonio-to-dallas': 'I-35',
    'dallas-to-fort-worth': 'I-30', 'fort-worth-to-dallas': 'I-30',
    'dallas-to-el-paso': 'I-20', 'el-paso-to-dallas': 'I-20',
    'houston-to-san-antonio': 'I-10', 'san-antonio-to-houston': 'I-10',
    'houston-to-austin': 'US-290', 'austin-to-houston': 'US-290',
    'austin-to-san-antonio': 'I-35', 'san-antonio-to-austin': 'I-35',
    'houston-to-galveston': 'I-45', 'galveston-to-houston': 'I-45',
    'houston-to-corpus-christi': 'US-59', 'corpus-christi-to-houston': 'US-59',
    'houston-to-new-orleans': 'I-10', 'new-orleans-to-houston': 'I-10',
    'dallas-to-oklahoma-city': 'I-35', 'oklahoma-city-to-dallas': 'I-35',
    
    # California
    'los-angeles-to-san-francisco': 'I-5', 'san-francisco-to-los-angeles': 'I-5',
    'los-angeles-to-san-diego': 'I-5', 'san-diego-to-los-angeles': 'I-5',
    'los-angeles-to-las-vegas': 'I-15', 'las-vegas-to-los-angeles': 'I-15',
    'los-angeles-to-phoenix': 'I-10', 'phoenix-to-los-angeles': 'I-10',
    'san-francisco-to-sacramento': 'I-80', 'sacramento-to-san-francisco': 'I-80',
    'san-francisco-to-san-jose': 'US-101', 'san-jose-to-san-francisco': 'US-101',
    'san-francisco-to-oakland': 'I-80', 'oakland-to-san-francisco': 'I-80',
    'los-angeles-to-bakersfield': 'I-5', 'bakersfield-to-los-angeles': 'I-5',
    'los-angeles-to-santa-barbara': 'US-101', 'santa-barbara-to-los-angeles': 'US-101',
    'san-diego-to-phoenix': 'I-8', 'phoenix-to-san-diego': 'I-8',
    
    # West
    'phoenix-to-las-vegas': 'US-93', 'las-vegas-to-phoenix': 'US-93',
    'phoenix-to-tucson': 'I-10', 'tucson-to-phoenix': 'I-10',
    'denver-to-salt-lake-city': 'I-70', 'salt-lake-city-to-denver': 'I-70',
    'denver-to-albuquerque': 'I-25', 'albuquerque-to-denver': 'I-25',
    'denver-to-colorado-springs': 'I-25', 'colorado-springs-to-denver': 'I-25',
    'las-vegas-to-salt-lake-city': 'I-15', 'salt-lake-city-to-las-vegas': 'I-15',
    
    # Pacific NW
    'seattle-to-portland': 'I-5', 'portland-to-seattle': 'I-5',
    'seattle-to-vancouver-wa': 'I-5', 'vancouver-wa-to-seattle': 'I-5',
    'portland-to-bend': 'US-97', 'bend-to-portland': 'US-97',
    'portland-to-boise': 'I-84', 'boise-to-portland': 'I-84',
    'seattle-to-spokane': 'I-90', 'spokane-to-seattle': 'I-90',
    
    # Midwest
    'detroit-to-cleveland': 'I-90', 'cleveland-to-detroit': 'I-90',
    'detroit-to-ann-arbor': 'I-94', 'ann-arbor-to-detroit': 'I-94',
    'cleveland-to-columbus': 'I-71', 'columbus-to-cleveland': 'I-71',
    'cleveland-to-pittsburgh': 'I-76', 'pittsburgh-to-cleveland': 'I-76',
    'cleveland-to-cincinnati': 'I-71', 'cincinnati-to-cleveland': 'I-71',
    'indianapolis-to-columbus': 'I-70', 'columbus-to-indianapolis': 'I-70',
    'indianapolis-to-louisville': 'I-65', 'louisville-to-indianapolis': 'I-65',
    'indianapolis-to-cincinnati': 'I-74', 'cincinnati-to-indianapolis': 'I-74',
    'minneapolis-to-milwaukee': 'I-94', 'milwaukee-to-minneapolis': 'I-94',
    'st-louis-to-kansas-city': 'I-70', 'kansas-city-to-st-louis': 'I-70',
    'st-louis-to-nashville': 'I-64', 'nashville-to-st-louis': 'I-64',
    'st-louis-to-memphis': 'I-55', 'memphis-to-st-louis': 'I-55',
    'st-louis-to-indianapolis': 'I-70', 'indianapolis-to-st-louis': 'I-70',
    
    # Northeast
    'new-york-to-boston': 'I-95', 'boston-to-new-york': 'I-95',
    'new-york-to-philadelphia': 'I-95', 'philadelphia-to-new-york': 'I-95',
    'new-york-to-washington-dc': 'I-95', 'washington-dc-to-new-york': 'I-95',
    'philadelphia-to-pittsburgh': 'I-76', 'pittsburgh-to-philadelphia': 'I-76',
    'boston-to-portland-me': 'I-95', 'portland-me-to-boston': 'I-95',
    'washington-dc-to-richmond': 'I-95', 'richmond-to-washington-dc': 'I-95',
    'washington-dc-to-baltimore': 'I-95', 'baltimore-to-washington-dc': 'I-95',
    
    # Long-haul cross-country
    'new-york-to-los-angeles': 'I-80', 'los-angeles-to-new-york': 'I-80',
    'new-york-to-chicago': 'I-80', 'chicago-to-new-york': 'I-80',
    'new-york-to-miami': 'I-95', 'miami-to-new-york': 'I-95',
    'los-angeles-to-houston': 'I-10', 'houston-to-los-angeles': 'I-10',
    'los-angeles-to-dallas': 'I-40', 'dallas-to-los-angeles': 'I-40',
    'los-angeles-to-denver': 'I-15', 'denver-to-los-angeles': 'I-15',
    'los-angeles-to-seattle': 'I-5', 'seattle-to-los-angeles': 'I-5',
    'san-francisco-to-seattle': 'I-5', 'seattle-to-san-francisco': 'I-5',
    'san-francisco-to-las-vegas': 'I-5', 'las-vegas-to-san-francisco': 'I-5',
    'seattle-to-houston': 'I-5', 'houston-to-seattle': 'I-10',
    'boston-to-miami': 'I-95', 'miami-to-boston': 'I-95',
    'boston-to-chicago': 'I-90', 'chicago-to-boston': 'I-90',
    'washington-dc-to-atlanta': 'I-85', 'atlanta-to-washington-dc': 'I-85',
    'washington-dc-to-chicago': 'I-70', 'chicago-to-washington-dc': 'I-70',
    'nashville-to-memphis': 'I-40', 'memphis-to-nashville': 'I-40',
    'dallas-to-atlanta': 'I-20', 'atlanta-to-dallas': 'I-20',
    'houston-to-atlanta': 'I-10', 'atlanta-to-houston': 'I-10',
    'denver-to-phoenix': 'I-25', 'phoenix-to-denver': 'I-25',
    'denver-to-dallas': 'I-25', 'dallas-to-denver': 'I-25',
    'denver-to-kansas-city': 'I-70', 'kansas-city-to-denver': 'I-70',
    'denver-to-omaha': 'I-76', 'omaha-to-denver': 'I-76',
    'minneapolis-to-denver': 'I-76', 'denver-to-minneapolis': 'I-76',
    'phoenix-to-albuquerque': 'I-40', 'albuquerque-to-phoenix': 'I-40',
    'phoenix-to-el-paso': 'I-10', 'el-paso-to-phoenix': 'I-10',
    'memphis-to-little-rock': 'I-40', 'little-rock-to-memphis': 'I-40',
    'memphis-to-birmingham': 'US-78', 'birmingham-to-memphis': 'US-78',
    'new-orleans-to-jackson': 'I-55', 'jackson-to-new-orleans': 'I-55',
    'new-orleans-to-atlanta': 'I-59', 'atlanta-to-new-orleans': 'I-59',
    'new-orleans-to-memphis': 'I-55', 'memphis-to-new-orleans': 'I-55',
    'new-orleans-to-baton-rouge': 'I-10', 'baton-rouge-to-new-orleans': 'I-10',
}

def determine_highway(from_slug, to_slug, coords):
    """Determine the most likely highway for a route based on geography."""
    route_key = f'{from_slug}-to-{to_slug}'
    
    # Check overrides first
    if route_key in ROUTE_OVERRIDES:
        return ROUTE_OVERRIDES[route_key]
    
    from_state = get_state(from_slug)
    to_state = get_state(to_slug)
    from_coord = get_coord(from_slug, coords)
    to_coord = get_coord(to_slug, coords)
    
    states = set(filter(None, [from_state, to_state]))
    
    # If we have coordinates, use them for precise routing
    if from_coord and to_coord:
        from_lat, from_lng = from_coord['lat'], from_coord['lng']
        to_lat, to_lng = to_coord['lat'], to_coord['lng']
        lat_diff = abs(from_lat - to_lat)
        lng_diff = abs(from_lng - to_lng)
        avg_lat = (from_lat + to_lat) / 2
        avg_lng = (from_lng + to_lng) / 2
        min_lng = min(from_lng, to_lng)
        max_lng = max(from_lng, to_lng)
        min_lat = min(from_lat, to_lat)
        max_lat = max(from_lat, to_lat)
        
        is_ew = lng_diff > lat_diff  # East-west dominant
        is_ns = lat_diff >= lng_diff  # North-south dominant
        
        # === WITHIN-STATE ROUTES ===
        
        # Florida within-state
        if states == {'FL'} or (len(states) == 1 and 'FL' in states):
            if from_lng > -81 and to_lng > -81:
                return 'I-95'  # East coast
            if from_lng < -81.5 and to_lng < -81.5:
                return 'I-75'  # West/central
            if is_ew and avg_lat > 27 and avg_lat < 29:
                return 'I-4'   # Central FL east-west corridor
            return 'I-95'
        
        # Texas within-state
        if states == {'TX'} or (len(states) == 1 and 'TX' in states):
            # Dallas-Houston is primarily N-S along I-45
            if (31 < max_lat and min_lat < 31 and -96.5 < avg_lng < -94.5):
                return 'I-45'
            # Austin/San Antonio - Dallas corridor (I-35)
            if -98 < avg_lng < -96 and is_ns:
                return 'I-35'
            # Houston - San Antonio (east-west southern TX)
            if is_ew and avg_lat < 30.5:
                return 'I-10'
            # Dallas - El Paso
            if is_ew and avg_lat > 31:
                return 'I-20'
            if is_ns:
                return 'I-35'
            return 'I-10'
        
        # California within-state
        if states == {'CA'} or (len(states) == 1 and 'CA' in states):
            # N-S routes
            if lat_diff > 1.5 and lat_diff > lng_diff * 0.5:
                return 'I-5'
            # E-W in SoCal
            if is_ew and avg_lat < 35:
                return 'I-10'
            # Bay Area local
            if lat_diff < 0.5 and lng_diff < 0.5 and avg_lat > 37:
                return 'US-101'
            return 'I-5'
        
        # Pacific NW within-state
        if states and states.issubset({'WA', 'OR'}):
            if is_ns or (lat_diff > 0.5):
                return 'I-5'
            if is_ew:
                if avg_lat > 46:
                    return 'I-90'
                return 'I-84'
            return 'I-5'
        
        # === MULTI-STATE / CROSS-COUNTRY ===
        
        # Northeast corridor (east coast, north of NC)
        ne_states = {'ME', 'NH', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA', 'DE', 'MD', 'DC', 'VA'}
        if states and states.issubset(ne_states):
            if is_ns or avg_lng > -76:
                if avg_lng > -76:
                    return 'I-95'
                # Western PA/NY
                if any(c < -78 for c in [from_lng, to_lng]):
                    if is_ew:
                        return 'I-76'
                    return 'I-81'
                return 'I-95'
            if is_ew:
                if avg_lat > 42:
                    return 'I-90'
                return 'I-76'
            return 'I-95'
        
        # Southeast N-S (GA, FL, AL, TN, NC, SC)
        se_ns_states = {'GA', 'FL', 'AL', 'TN', 'NC', 'SC'}
        if states and len(states.intersection(se_ns_states)) >= 1 and is_ns:
            if avg_lng > -82:
                return 'I-95'  # East coast
            elif avg_lng > -85:
                return 'I-75'  # Central (Atlanta-Miami corridor)
            else:
                return 'I-65'  # West (Nashville-Birmingham-Mobile)
        
        # General coordinate-based routing
        if is_ew:
            # East-west routes by latitude band
            if avg_lat > 43:
                return 'I-90'  # Northern (Boston-Seattle)
            elif avg_lat > 41:
                # Chicago corridor
                if min_lng > -90:
                    return 'I-80'
                return 'I-94' if max_lng > -87 and min_lng > -94 else 'I-90'
            elif avg_lat > 39:
                return 'I-80'  # Mid-northern (NYC-SF)
            elif avg_lat > 37:
                return 'I-70'  # Central (DC-Denver-UT)
            elif avg_lat > 35:
                return 'I-40'  # South-central (OKC-Albuquerque-LA)
            elif avg_lat > 32:
                return 'I-20'  # South (Dallas-Atlanta)
            else:
                return 'I-10'  # Southern (LA-Houston-Jacksonville)
        else:
            # North-south routes by longitude band
            if avg_lng > -76:
                return 'I-95'  # East coast
            elif avg_lng > -81:
                return 'I-85'  # Piedmont (DC-Charlotte-Atlanta)
            elif avg_lng > -84.5:
                return 'I-75'  # Southeast (Detroit-Atlanta-Miami)
            elif avg_lng > -88:
                return 'I-65'  # Central-east (Chicago-Nashville-Birmingham)
            elif avg_lng > -91:
                return 'I-55'  # Mississippi valley (Chicago-Memphis-NOLA)
            elif avg_lng > -97:
                return 'I-35'  # Central (Minneapolis-Dallas)
            elif avg_lng > -105:
                return 'I-25'  # Mountain (Denver-Albuquerque)
            elif avg_lng > -115:
                return 'I-15'  # Inter-mountain (SLC-Vegas-LA)
            else:
                return 'I-5'   # West coast
    
    # State-based fallbacks (no coords available)
    if from_state and to_state:
        se_states = {'GA', 'SC', 'NC', 'VA', 'TN', 'AL', 'FL'}
        mw_states = {'OH', 'IN', 'IL', 'MI', 'WI', 'MN', 'IA', 'MO'}
        ne_states2 = {'ME', 'NH', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA', 'DE', 'MD', 'DC', 'VA'}
        
        if states.issubset(ne_states2):
            return 'I-95'
        if states.issubset(se_states):
            return 'I-75'
        if states.issubset(mw_states):
            return 'I-80'
        if 'TX' in states:
            return 'I-10'
        if 'CA' in states:
            return 'I-5'
        if states.intersection({'WA', 'OR'}):
            return 'I-5'
    
    # Ultimate fallback
    return 'I-95'


# ── TASK 1: Fix "via Interstate" ──────────────────────────────────────────

def fix_interstate():
    """Fix all 'via Interstate' and '<span>Interstate</span>' occurrences."""
    print("=== TASK 1: Fixing 'via Interstate' ===")
    
    hw_data = load_all_highways()
    coords = load_coords()
    
    # Find all affected files
    result = subprocess.run(['grep', '-rl', 'Interstate', os.path.join(BASE, 'route')], 
                          capture_output=True, text=True)
    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    
    print(f"Found {len(files)} files with 'Interstate'")
    
    fixed_count = 0
    data_match = 0
    geo_match = 0
    
    for filepath in files:
        slug = filepath.replace(ROUTE_DIR + '/', '').replace('/index.html', '')
        parts = slug.split('-to-')
        if len(parts) != 2:
            continue
        
        from_slug, to_slug = parts[0], parts[1]
        
        # Try data first
        highway = hw_data.get(slug)
        if highway:
            data_match += 1
        else:
            # Also try reverse
            reverse_slug = f"{to_slug}-to-{from_slug}"
            highway = hw_data.get(reverse_slug)
            if highway:
                # Reverse direction indicator
                if highway.endswith(' N'):
                    highway = highway[:-2] + ' S'
                elif highway.endswith(' S'):
                    highway = highway[:-2] + ' N'
                elif highway.endswith(' E'):
                    highway = highway[:-2] + ' W'
                elif highway.endswith(' W'):
                    highway = highway[:-2] + ' E'
                data_match += 1
        
        if not highway:
            highway = determine_highway(from_slug, to_slug, coords)
            geo_match += 1
        
        # Clean highway name (remove direction for display)
        hw_display = highway.split(' ')[0] if highway else 'Interstate'
        
        if hw_display == 'Interstate':
            continue
        
        # Read and fix the file
        with open(filepath, 'r') as f:
            content = f.read()
        
        original = content
        
        # Replace all instances
        # 1. "via Interstate." and "via Interstate" in various contexts
        content = content.replace('via Interstate.', f'via {hw_display}.')
        content = content.replace('via Interstate,', f'via {hw_display},')
        content = content.replace('via Interstate"', f'via {hw_display}"')
        content = content.replace('via Interstate<', f'via {hw_display}<')
        
        # 2. Subtitle: <p class="subtitle">via Interstate</p>
        content = content.replace('>via Interstate</p>', f'>via {hw_display}</p>')
        
        # 3. Trip details: <span>Interstate</span>
        content = content.replace('<span>Interstate</span>', f'<span>{hw_display}</span>')
        
        # 4. Route Tips: Interstate
        content = content.replace('Route Tips: Interstate</h3>', f'Route Tips: {hw_display}</h3>')
        
        # Catch any remaining standalone "via Interstate" 
        content = content.replace('via Interstate', f'via {hw_display}')
        
        if content != original:
            with open(filepath, 'w') as f:
                f.write(content)
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files")
    print(f"  From data: {data_match}, From geo logic: {geo_match}")
    return fixed_count


# ── TASK 2: Fix E-ZPass references ──────────────────────────────────────

def fix_ezpass():
    """Fix E-ZPass references on route pages."""
    print("\n=== TASK 2: Fixing E-ZPass references ===")
    
    result = subprocess.run(['grep', '-rl', 'E-ZPass', os.path.join(BASE, 'route')],
                          capture_output=True, text=True)
    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    
    print(f"Found {len(files)} files with E-ZPass")
    
    kept = 0
    replaced = 0
    
    for filepath in files:
        slug = filepath.replace(ROUTE_DIR + '/', '').replace('/index.html', '')
        parts = slug.split('-to-')
        if len(parts) != 2:
            continue
        
        from_slug, to_slug = parts[0], parts[1]
        from_state = get_state(from_slug)
        to_state = get_state(to_slug)
        
        states = set(filter(None, [from_state, to_state]))
        
        # Check if any state involved is an E-ZPass state
        if states.intersection(EZPASS_STATES):
            kept += 1
            continue
        
        # Determine appropriate replacement
        replacement = None
        if 'FL' in states:
            replacement = 'SunPass'
        elif 'TX' in states:
            replacement = 'TxTag'
        elif 'CA' in states:
            replacement = 'FasTrak'
        elif 'CO' in states:
            replacement = 'ExpressToll'
        elif 'WA' in states:
            replacement = 'Good To Go!'
        elif 'GA' in states:
            replacement = 'Peach Pass'
        elif 'OK' in states:
            replacement = 'PikePass'
        elif 'KS' in states:
            replacement = 'K-TAG'
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        original = content
        
        if replacement:
            # Replace E-ZPass with specific transponder
            content = content.replace(
                'Consider getting an E-ZPass or similar transponder for faster toll payment.',
                f'Consider getting a {replacement} transponder for faster toll payment.'
            )
            content = content.replace(
                'an E-ZPass or similar transponder',
                f'a {replacement} transponder' if replacement[0] not in 'AEIOU' else f'an {replacement} transponder'
            )
            # Catch other patterns
            content = content.replace('E-ZPass', replacement)
        else:
            # Generic replacement for states without a specific transponder
            content = content.replace(
                'Consider getting an E-ZPass or similar transponder for faster toll payment.',
                'Check with the local toll authority for transponder options to speed up toll payment.'
            )
            content = content.replace(
                'an E-ZPass or similar transponder',
                'a toll transponder'
            )
            content = content.replace('E-ZPass', 'toll transponder')
        
        if content != original:
            with open(filepath, 'w') as f:
                f.write(content)
            replaced += 1
    
    print(f"Kept E-ZPass on {kept} files (NE states)")
    print(f"Replaced E-ZPass on {replaced} files")
    return replaced


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    fix1 = fix_interstate()
    fix2 = fix_ezpass()
    print(f"\n=== DONE ===")
    print(f"Task 1: Fixed {fix1} route pages (Interstate -> specific highway)")
    print(f"Task 2: Fixed {fix2} route pages (E-ZPass -> appropriate transponder)")
