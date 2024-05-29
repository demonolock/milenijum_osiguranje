import csv
import time
import gmplot
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from requests.exceptions import ReadTimeout


def get_lat_long(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Geocoding failed for address: {address}")
            return None, None
    except GeocoderTimedOut as e:
        print(f"Geocoding error for address {address}: {e}")
        return None, None
    except GeocoderServiceError as e:
        print(f"Geocoding error for address {address}: {e}")
        return None, None
    except ReadTimeout as e:
        print(f"Geocoding error for address {address}: {e}")
        return None, None


# Target location coordinates for Novi Sad
target_location = (45.2671, 19.8335)

# Read addresses from CSV file
addresses = []
with open('addresses.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        addresses.append(row[0])

# Calculate distances for each address
address_distances = {}
for address in addresses:
    latitude, longitude = get_lat_long(address)
    if latitude is not None and longitude is not None:
        address_location = (latitude, longitude)
        distance = geodesic(target_location, address_location).kilometers
        address_distances[address] = distance

# Sort addresses by distance
sorted_addresses = sorted(address_distances.items(), key=lambda x: x[1])

# Initialize the map at a certain location (latitude, longitude)
gmap = gmplot.GoogleMapPlotter(45.2671, 19.8335, 10)  # Coordinates for Novi Sad

# Add a marker for each address, with different colors based on proximity
for idx, (address, distance) in enumerate(sorted_addresses):
    color = 'red' if idx < len(sorted_addresses) // 2 else 'blue'
    latitude, longitude = get_lat_long(address)
    if latitude is not None and longitude is not None:
        gmap.marker(latitude, longitude, color)

# Save the map to an HTML file
gmap.draw("map.html")
    
print("Map generated and saved as map.html")
