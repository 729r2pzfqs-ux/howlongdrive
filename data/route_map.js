const ROUTE_MAP = {
  "ATL": [
    "Atlanta",
    "Downtown Atlanta"
  ],
  "Albany": [
    "New York"
  ],
  "Albuquerque": [
    "Denver",
    "El Paso",
    "Phoenix",
    "Santa Fe"
  ],
  "Alexandria": [
    "Washington DC"
  ],
  "Alpharetta": [
    "Atlanta"
  ],
  "Anaheim": [
    "LAX",
    "Los Angeles"
  ],
  "Anchorage": [
    "Fairbanks"
  ],
  "Arches National Park": [
    "Salt Lake City"
  ],
  "Arlington": [
    "DFW",
    "Dallas",
    "Washington DC"
  ],
  "Arvada": [
    "Denver"
  ],
  "Aspen": [
    "Denver"
  ],
  "Atlanta": [
    "ATL",
    "Alpharetta",
    "Austin",
    "Baltimore",
    "Birmingham",
    "Boston",
    "Charlotte",
    "Chattanooga",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Decatur",
    "Denver",
    "Detroit",
    "Houston",
    "Kennesaw",
    "Knoxville",
    "Las Vegas",
    "Los Angeles",
    "Marietta",
    "Memphis",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Roswell",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Sandy Springs",
    "Savannah",
    "Seattle",
    "Tallahassee",
    "Tampa",
    "Washington DC"
  ],
  "Atlantic City": [
    "New York"
  ],
  "Aurora": [
    "Chicago",
    "Denver"
  ],
  "Austin": [
    "Atlanta",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "BOS": [
    "Boston",
    "Cambridge"
  ],
  "BWI": [
    "Baltimore",
    "Washington DC"
  ],
  "Baltimore": [
    "Atlanta",
    "Austin",
    "BWI",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "Baytown": [
    "Houston"
  ],
  "Bellevue": [
    "SEA",
    "Seattle"
  ],
  "Berkeley": [
    "San Francisco"
  ],
  "Bethesda": [
    "Washington DC"
  ],
  "Big Bear Lake": [
    "Los Angeles"
  ],
  "Billings": [
    "Boise",
    "Denver"
  ],
  "Birmingham": [
    "Atlanta",
    "Jackson",
    "Mobile",
    "Nashville",
    "New Orleans"
  ],
  "Boca Raton": [
    "Miami"
  ],
  "Boise": [
    "Billings",
    "Missoula",
    "Portland",
    "Salt Lake City",
    "Seattle",
    "Spokane"
  ],
  "Boston": [
    "Atlanta",
    "Austin",
    "BOS",
    "Baltimore",
    "Brookline",
    "Cambridge",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Hartford",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Lowell",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Newton",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Providence",
    "Quincy",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Somerville",
    "Tampa",
    "Washington DC",
    "Worcester"
  ],
  "Boulder": [
    "DEN",
    "Denver"
  ],
  "Breckenridge": [
    "Denver"
  ],
  "Brookline": [
    "Boston"
  ],
  "Brooklyn": [
    "JFK"
  ],
  "Burbank": [
    "Los Angeles"
  ],
  "Cambridge": [
    "BOS",
    "Boston"
  ],
  "Camden": [
    "Philadelphia"
  ],
  "Carmel": [
    "San Francisco"
  ],
  "Chandler": [
    "Phoenix"
  ],
  "Charleston": [
    "Charlotte",
    "Myrtle Beach",
    "Savannah"
  ],
  "Charlotte": [
    "Atlanta",
    "Charleston",
    "Myrtle Beach",
    "Raleigh"
  ],
  "Chattanooga": [
    "Atlanta",
    "Knoxville",
    "Nashville"
  ],
  "Cherry Hill": [
    "Philadelphia"
  ],
  "Chicago": [
    "Atlanta",
    "Aurora",
    "Austin",
    "Baltimore",
    "Boston",
    "Cleveland",
    "Dallas",
    "Denver",
    "Des Moines",
    "Detroit",
    "Evanston",
    "Grand Rapids",
    "Green Bay",
    "Houston",
    "Indianapolis",
    "Joliet",
    "Kansas City",
    "Lake Geneva",
    "Las Vegas",
    "Los Angeles",
    "MDW",
    "Madison",
    "Miami",
    "Milwaukee",
    "Minneapolis",
    "Naperville",
    "Nashville",
    "New Orleans",
    "New York",
    "ORD",
    "Oak Park",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Schaumburg",
    "Seattle",
    "St Louis",
    "Tampa",
    "Washington DC",
    "Waukegan",
    "Wisconsin Dells"
  ],
  "Cincinnati": [
    "Columbus",
    "Lexington",
    "Louisville"
  ],
  "Clearwater Beach": [
    "Orlando"
  ],
  "Cleveland": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Columbus",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "Colorado Springs": [
    "Denver"
  ],
  "Columbus": [
    "Cincinnati",
    "Cleveland"
  ],
  "Coral Gables": [
    "Miami"
  ],
  "DCA": [
    "Washington DC"
  ],
  "DEN": [
    "Boulder",
    "Denver"
  ],
  "DFW": [
    "Arlington",
    "Dallas",
    "Fort Worth"
  ],
  "Dallas": [
    "Arlington",
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "DFW",
    "Denton",
    "Denver",
    "Detroit",
    "Fort Worth",
    "Frisco",
    "Houston",
    "Irving",
    "Kansas City",
    "Las Vegas",
    "Little Rock",
    "Los Angeles",
    "McKinney",
    "Memphis",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Oklahoma City",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Plano",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Tulsa",
    "Washington DC"
  ],
  "Daly City": [
    "San Francisco"
  ],
  "Daytona Beach": [
    "Orlando"
  ],
  "Death Valley": [
    "Las Vegas"
  ],
  "Decatur": [
    "Atlanta"
  ],
  "Denton": [
    "Dallas"
  ],
  "Denver": [
    "Albuquerque",
    "Arvada",
    "Aspen",
    "Atlanta",
    "Aurora",
    "Austin",
    "Baltimore",
    "Billings",
    "Boston",
    "Boulder",
    "Breckenridge",
    "Chicago",
    "Cleveland",
    "Colorado Springs",
    "DEN",
    "Dallas",
    "Detroit",
    "Estes Park",
    "Fort Collins",
    "Houston",
    "Kansas City",
    "Lakewood",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Omaha",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Rapid City",
    "Rocky Mountain NP",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Santa Fe",
    "Seattle",
    "Tampa",
    "Thornton",
    "Vail",
    "Washington DC",
    "Westminster",
    "Wichita"
  ],
  "Des Moines": [
    "Chicago",
    "Kansas City",
    "Minneapolis",
    "Omaha"
  ],
  "Detroit": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Grand Rapids",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "Disney World": [
    "MCO",
    "Orlando"
  ],
  "Disneyland": [
    "Los Angeles"
  ],
  "Dollywood": [
    "Nashville"
  ],
  "Downtown Atlanta": [
    "ATL"
  ],
  "Downtown Chicago": [
    "ORD"
  ],
  "Duluth": [
    "Minneapolis"
  ],
  "EWR": [
    "Manhattan"
  ],
  "El Paso": [
    "Albuquerque",
    "San Antonio",
    "Tucson"
  ],
  "Estes Park": [
    "Denver"
  ],
  "Evanston": [
    "Chicago"
  ],
  "Everett": [
    "Seattle"
  ],
  "Everglades": [
    "Miami"
  ],
  "FLL": [
    "Fort Lauderdale",
    "Miami"
  ],
  "Fairbanks": [
    "Anchorage"
  ],
  "Fargo": [
    "Minneapolis"
  ],
  "Fort Collins": [
    "Denver"
  ],
  "Fort Lauderdale": [
    "FLL",
    "MIA",
    "Miami"
  ],
  "Fort Worth": [
    "DFW",
    "Dallas"
  ],
  "Fremont": [
    "San Francisco"
  ],
  "Fresno": [
    "Los Angeles"
  ],
  "Frisco": [
    "Dallas"
  ],
  "Galveston": [
    "Houston"
  ],
  "Gatlinburg": [
    "Knoxville",
    "Nashville"
  ],
  "Gilbert": [
    "Phoenix"
  ],
  "Glendale": [
    "Los Angeles",
    "Phoenix"
  ],
  "Grand Canyon": [
    "Las Vegas",
    "Phoenix"
  ],
  "Grand Rapids": [
    "Chicago",
    "Detroit"
  ],
  "Great Smoky Mountains": [
    "Nashville"
  ],
  "Green Bay": [
    "Chicago",
    "Madison",
    "Milwaukee"
  ],
  "HOU": [
    "Houston"
  ],
  "Hamptons": [
    "New York"
  ],
  "Hartford": [
    "Boston",
    "New York"
  ],
  "Hialeah": [
    "Miami"
  ],
  "Hoboken": [
    "New York"
  ],
  "Hollywood": [
    "LAX",
    "Miami"
  ],
  "Honolulu": [
    "Pearl Harbor",
    "Waikiki"
  ],
  "Hoover Dam": [
    "Las Vegas"
  ],
  "Houston": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Baytown",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Galveston",
    "HOU",
    "IAH",
    "Katy",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Oklahoma City",
    "Orlando",
    "Pasadena",
    "Pearland",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Sugar Land",
    "Tampa",
    "The Woodlands",
    "Washington DC"
  ],
  "IAD": [
    "Washington DC"
  ],
  "IAH": [
    "Houston"
  ],
  "Indianapolis": [
    "Chicago",
    "Louisville"
  ],
  "Irvine": [
    "Los Angeles"
  ],
  "Irving": [
    "Dallas"
  ],
  "JFK": [
    "Brooklyn",
    "Manhattan",
    "Times Square"
  ],
  "Jackson": [
    "Birmingham",
    "Memphis",
    "New Orleans"
  ],
  "Jacksonville": [
    "Orlando",
    "Savannah",
    "Tallahassee",
    "Tampa"
  ],
  "Jersey City": [
    "New York"
  ],
  "Joliet": [
    "Chicago"
  ],
  "Joshua Tree": [
    "Los Angeles"
  ],
  "Kansas City": [
    "Chicago",
    "Dallas",
    "Denver",
    "Des Moines",
    "Minneapolis",
    "Oklahoma City",
    "Omaha",
    "St Louis",
    "Tulsa",
    "Wichita"
  ],
  "Katy": [
    "Houston"
  ],
  "Kennedy Space Center": [
    "Orlando"
  ],
  "Kennesaw": [
    "Atlanta"
  ],
  "Kent": [
    "Seattle"
  ],
  "Key West": [
    "Miami"
  ],
  "King of Prussia": [
    "Philadelphia"
  ],
  "Kirkland": [
    "Seattle"
  ],
  "Knoxville": [
    "Atlanta",
    "Chattanooga",
    "Gatlinburg",
    "Nashville"
  ],
  "LAS": [
    "Las Vegas",
    "Las Vegas Strip"
  ],
  "LAX": [
    "Anaheim",
    "Hollywood",
    "Long Beach",
    "Los Angeles",
    "Santa Monica"
  ],
  "LGA": [
    "Manhattan"
  ],
  "Lake Geneva": [
    "Chicago"
  ],
  "Lake Tahoe": [
    "Reno",
    "San Francisco"
  ],
  "Lakewood": [
    "Denver"
  ],
  "Las Vegas": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Death Valley",
    "Denver",
    "Detroit",
    "Grand Canyon",
    "Hoover Dam",
    "Houston",
    "LAS",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Reno",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC",
    "Zion National Park"
  ],
  "Las Vegas Strip": [
    "LAS"
  ],
  "Leavenworth": [
    "Seattle"
  ],
  "Legoland": [
    "San Diego"
  ],
  "Lexington": [
    "Cincinnati",
    "Louisville"
  ],
  "Little Rock": [
    "Dallas",
    "Memphis",
    "New Orleans"
  ],
  "Long Beach": [
    "LAX",
    "Los Angeles"
  ],
  "Long Island City": [
    "New York"
  ],
  "Los Angeles": [
    "Anaheim",
    "Atlanta",
    "Austin",
    "Baltimore",
    "Big Bear Lake",
    "Boston",
    "Burbank",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Disneyland",
    "Fresno",
    "Glendale",
    "Houston",
    "Irvine",
    "Joshua Tree",
    "LAX",
    "Las Vegas",
    "Long Beach",
    "Malibu",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Ontario",
    "Orlando",
    "Palm Springs",
    "Pasadena",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Sacramento",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Santa Barbara",
    "Santa Monica",
    "Seattle",
    "Tampa",
    "Universal Studios",
    "Washington DC"
  ],
  "Louisville": [
    "Cincinnati",
    "Indianapolis",
    "Lexington",
    "Nashville"
  ],
  "Lowell": [
    "Boston"
  ],
  "MCO": [
    "Disney World",
    "Orlando",
    "Universal Orlando"
  ],
  "MDW": [
    "Chicago"
  ],
  "MIA": [
    "Fort Lauderdale",
    "Miami",
    "Miami Beach"
  ],
  "Madison": [
    "Chicago",
    "Green Bay",
    "Milwaukee",
    "Minneapolis"
  ],
  "Malibu": [
    "Los Angeles"
  ],
  "Manhattan": [
    "EWR",
    "JFK",
    "LGA"
  ],
  "Marietta": [
    "Atlanta"
  ],
  "McKinney": [
    "Dallas"
  ],
  "Memphis": [
    "Atlanta",
    "Dallas",
    "Jackson",
    "Little Rock",
    "Nashville",
    "New Orleans",
    "St Louis"
  ],
  "Mesa": [
    "Phoenix"
  ],
  "Miami": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boca Raton",
    "Boston",
    "Chicago",
    "Cleveland",
    "Coral Gables",
    "Dallas",
    "Denver",
    "Detroit",
    "Everglades",
    "FLL",
    "Fort Lauderdale",
    "Hialeah",
    "Hollywood",
    "Houston",
    "Key West",
    "Las Vegas",
    "Los Angeles",
    "MIA",
    "Miami Beach",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "South Beach",
    "Tampa",
    "Washington DC",
    "West Palm Beach"
  ],
  "Miami Beach": [
    "MIA",
    "Miami"
  ],
  "Milwaukee": [
    "Chicago",
    "Green Bay",
    "Madison"
  ],
  "Minneapolis": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Des Moines",
    "Detroit",
    "Duluth",
    "Fargo",
    "Houston",
    "Kansas City",
    "Las Vegas",
    "Los Angeles",
    "Madison",
    "Miami",
    "Nashville",
    "New Orleans",
    "New York",
    "Omaha",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Sioux Falls",
    "Tampa",
    "Washington DC"
  ],
  "Missoula": [
    "Boise",
    "Spokane"
  ],
  "Mobile": [
    "Birmingham",
    "New Orleans",
    "Pensacola"
  ],
  "Monterey": [
    "San Francisco"
  ],
  "Mount Rainier": [
    "Seattle"
  ],
  "Mount Rushmore": [
    "Rapid City"
  ],
  "Muir Woods": [
    "San Francisco"
  ],
  "Myrtle Beach": [
    "Charleston",
    "Charlotte",
    "Wilmington"
  ],
  "Napa Valley": [
    "San Francisco"
  ],
  "Naperville": [
    "Chicago"
  ],
  "Nashville": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Birmingham",
    "Boston",
    "Chattanooga",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Dollywood",
    "Gatlinburg",
    "Great Smoky Mountains",
    "Houston",
    "Knoxville",
    "Las Vegas",
    "Los Angeles",
    "Louisville",
    "Memphis",
    "Miami",
    "Minneapolis",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "New Orleans": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Birmingham",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Jackson",
    "Las Vegas",
    "Little Rock",
    "Los Angeles",
    "Memphis",
    "Miami",
    "Minneapolis",
    "Mobile",
    "Nashville",
    "New York",
    "Orlando",
    "Pensacola",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "New Rochelle": [
    "New York"
  ],
  "New York": [
    "Albany",
    "Atlanta",
    "Atlantic City",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Hamptons",
    "Hartford",
    "Hoboken",
    "Houston",
    "Jersey City",
    "Las Vegas",
    "Long Island City",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New Rochelle",
    "Newark",
    "Niagara Falls",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Stamford",
    "Statue of Liberty",
    "Tampa",
    "Washington DC",
    "White Plains",
    "Yonkers"
  ],
  "Newark": [
    "New York"
  ],
  "Newton": [
    "Boston"
  ],
  "Niagara Falls": [
    "New York"
  ],
  "Norfolk": [
    "Richmond",
    "Virginia Beach",
    "Washington DC"
  ],
  "OAK": [
    "Oakland",
    "San Francisco"
  ],
  "ORD": [
    "Chicago",
    "Downtown Chicago"
  ],
  "Oak Park": [
    "Chicago"
  ],
  "Oakland": [
    "OAK",
    "San Francisco"
  ],
  "Oklahoma City": [
    "Dallas",
    "Houston",
    "Kansas City",
    "Tulsa",
    "Wichita"
  ],
  "Olympic National Park": [
    "Seattle"
  ],
  "Omaha": [
    "Denver",
    "Des Moines",
    "Kansas City",
    "Minneapolis",
    "Sioux Falls"
  ],
  "Ontario": [
    "Los Angeles"
  ],
  "Orlando": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Clearwater Beach",
    "Cleveland",
    "Dallas",
    "Daytona Beach",
    "Denver",
    "Detroit",
    "Disney World",
    "Houston",
    "Jacksonville",
    "Kennedy Space Center",
    "Las Vegas",
    "Los Angeles",
    "MCO",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Universal Orlando",
    "Washington DC"
  ],
  "PHX": [
    "Phoenix",
    "Scottsdale",
    "Tempe"
  ],
  "Palm Springs": [
    "Los Angeles"
  ],
  "Palo Alto": [
    "SFO",
    "San Francisco"
  ],
  "Park City": [
    "Salt Lake City"
  ],
  "Pasadena": [
    "Houston",
    "Los Angeles"
  ],
  "Pearl Harbor": [
    "Honolulu"
  ],
  "Pearland": [
    "Houston"
  ],
  "Pensacola": [
    "Mobile",
    "New Orleans",
    "Tallahassee"
  ],
  "Peoria": [
    "Phoenix"
  ],
  "Philadelphia": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Camden",
    "Cherry Hill",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "King of Prussia",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Phoenix",
    "Pittsburgh",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Trenton",
    "Washington DC",
    "Wilmington"
  ],
  "Phoenix": [
    "Albuquerque",
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chandler",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Gilbert",
    "Glendale",
    "Grand Canyon",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Mesa",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "PHX",
    "Peoria",
    "Philadelphia",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Scottsdale",
    "Seattle",
    "Sedona",
    "Tampa",
    "Tempe",
    "Tucson",
    "Washington DC"
  ],
  "Pittsburgh": [
    "Philadelphia"
  ],
  "Plano": [
    "Dallas"
  ],
  "Portland": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boise",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Spokane",
    "Tampa",
    "Washington DC"
  ],
  "Providence": [
    "Boston"
  ],
  "Quincy": [
    "Boston"
  ],
  "Raleigh": [
    "Charlotte",
    "Richmond"
  ],
  "Rapid City": [
    "Denver",
    "Mount Rushmore"
  ],
  "Redmond": [
    "Seattle"
  ],
  "Reno": [
    "Lake Tahoe",
    "Las Vegas",
    "Sacramento",
    "San Francisco"
  ],
  "Renton": [
    "Seattle"
  ],
  "Reston": [
    "Washington DC"
  ],
  "Richmond": [
    "Norfolk",
    "Raleigh",
    "Virginia Beach",
    "Washington DC"
  ],
  "Rockville": [
    "Washington DC"
  ],
  "Rocky Mountain NP": [
    "Denver"
  ],
  "Roswell": [
    "Atlanta"
  ],
  "SEA": [
    "Bellevue",
    "Seattle",
    "Tacoma"
  ],
  "SFO": [
    "Palo Alto",
    "San Francisco",
    "San Jose"
  ],
  "Sacramento": [
    "Los Angeles",
    "Reno",
    "San Francisco",
    "San Jose"
  ],
  "Salt Lake City": [
    "Arches National Park",
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boise",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Park City",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Sundance",
    "Tampa",
    "Washington DC"
  ],
  "San Antonio": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "El Paso",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "San Diego": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Legoland",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego Zoo",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Tijuana",
    "Tucson",
    "Washington DC"
  ],
  "San Diego Zoo": [
    "San Diego"
  ],
  "San Francisco": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Berkeley",
    "Boston",
    "Carmel",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Daly City",
    "Denver",
    "Detroit",
    "Fremont",
    "Houston",
    "Lake Tahoe",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Monterey",
    "Muir Woods",
    "Napa Valley",
    "Nashville",
    "New Orleans",
    "New York",
    "OAK",
    "Oakland",
    "Orlando",
    "Palo Alto",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Reno",
    "SFO",
    "Sacramento",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Jose",
    "San Mateo",
    "Seattle",
    "Tampa",
    "Walnut Creek",
    "Washington DC",
    "Yosemite"
  ],
  "San Jose": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "SFO",
    "Sacramento",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "Seattle",
    "Tampa",
    "Washington DC"
  ],
  "San Mateo": [
    "San Francisco"
  ],
  "Sandy Springs": [
    "Atlanta"
  ],
  "Santa Barbara": [
    "Los Angeles"
  ],
  "Santa Fe": [
    "Albuquerque",
    "Denver",
    "Taos"
  ],
  "Santa Monica": [
    "LAX",
    "Los Angeles"
  ],
  "Savannah": [
    "Atlanta",
    "Charleston",
    "Jacksonville"
  ],
  "Schaumburg": [
    "Chicago"
  ],
  "Scottsdale": [
    "PHX",
    "Phoenix"
  ],
  "Seattle": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Bellevue",
    "Boise",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Everett",
    "Houston",
    "Kent",
    "Kirkland",
    "Las Vegas",
    "Leavenworth",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Mount Rainier",
    "Nashville",
    "New Orleans",
    "New York",
    "Olympic National Park",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Redmond",
    "Renton",
    "SEA",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Snoqualmie Falls",
    "Spokane",
    "Tacoma",
    "Tampa",
    "Vancouver",
    "Washington DC"
  ],
  "Sedona": [
    "Phoenix"
  ],
  "Silver Spring": [
    "Washington DC"
  ],
  "Sioux Falls": [
    "Minneapolis",
    "Omaha"
  ],
  "Snoqualmie Falls": [
    "Seattle"
  ],
  "Somerville": [
    "Boston"
  ],
  "South Beach": [
    "Miami"
  ],
  "Spokane": [
    "Boise",
    "Missoula",
    "Portland",
    "Seattle"
  ],
  "St Louis": [
    "Chicago",
    "Kansas City",
    "Memphis"
  ],
  "Stamford": [
    "New York"
  ],
  "Statue of Liberty": [
    "New York"
  ],
  "Sugar Land": [
    "Houston"
  ],
  "Sundance": [
    "Salt Lake City"
  ],
  "Tacoma": [
    "SEA",
    "Seattle"
  ],
  "Tallahassee": [
    "Atlanta",
    "Jacksonville",
    "Pensacola"
  ],
  "Tampa": [
    "Atlanta",
    "Austin",
    "Baltimore",
    "Boston",
    "Chicago",
    "Cleveland",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "Jacksonville",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Washington DC"
  ],
  "Taos": [
    "Santa Fe"
  ],
  "Tempe": [
    "PHX",
    "Phoenix"
  ],
  "The Woodlands": [
    "Houston"
  ],
  "Thornton": [
    "Denver"
  ],
  "Tijuana": [
    "San Diego"
  ],
  "Times Square": [
    "JFK"
  ],
  "Trenton": [
    "Philadelphia"
  ],
  "Tucson": [
    "El Paso",
    "Phoenix",
    "San Diego"
  ],
  "Tulsa": [
    "Dallas",
    "Kansas City",
    "Oklahoma City"
  ],
  "Tysons": [
    "Washington DC"
  ],
  "Universal Orlando": [
    "MCO",
    "Orlando"
  ],
  "Universal Studios": [
    "Los Angeles"
  ],
  "Vail": [
    "Denver"
  ],
  "Vancouver": [
    "Seattle"
  ],
  "Virginia Beach": [
    "Norfolk",
    "Richmond"
  ],
  "Waikiki": [
    "Honolulu"
  ],
  "Walnut Creek": [
    "San Francisco"
  ],
  "Washington DC": [
    "Alexandria",
    "Arlington",
    "Atlanta",
    "Austin",
    "BWI",
    "Baltimore",
    "Bethesda",
    "Boston",
    "Chicago",
    "Cleveland",
    "DCA",
    "Dallas",
    "Denver",
    "Detroit",
    "Houston",
    "IAD",
    "Las Vegas",
    "Los Angeles",
    "Miami",
    "Minneapolis",
    "Nashville",
    "New Orleans",
    "New York",
    "Norfolk",
    "Orlando",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Reston",
    "Richmond",
    "Rockville",
    "Salt Lake City",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Silver Spring",
    "Tampa",
    "Tysons"
  ],
  "Waukegan": [
    "Chicago"
  ],
  "West Palm Beach": [
    "Miami"
  ],
  "Westminster": [
    "Denver"
  ],
  "White Plains": [
    "New York"
  ],
  "Wichita": [
    "Denver",
    "Kansas City",
    "Oklahoma City"
  ],
  "Wilmington": [
    "Myrtle Beach",
    "Philadelphia"
  ],
  "Wisconsin Dells": [
    "Chicago"
  ],
  "Worcester": [
    "Boston"
  ],
  "Yonkers": [
    "New York"
  ],
  "Yosemite": [
    "San Francisco"
  ],
  "Zion National Park": [
    "Las Vegas"
  ]
};