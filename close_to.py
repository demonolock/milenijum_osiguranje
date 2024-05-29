import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Add your address here
target_address = "Srbija, Novi Sad, Braće Ribnikar 7"
geolocator = Nominatim(user_agent="geoapiExercises")
target_location = geolocator.geocode(target_address)
target_lat = target_location.latitude
target_lon = target_location.longitude

# Initialize an empty list to store addresses
addresses = []

# Read addresses from CSV file
with open('addresses.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        address = row[0] + ', ' + row[1] + ', ' + row[2]
        addresses.append(address)

# Calculate distances for each address
address_distances = {}
for address in addresses:
    location = geolocator.geocode(address)
    if location:
        address_lat = location.latitude
        address_lon = location.longitude
        distance = geodesic((target_lat, target_lon), (address_lat, address_lon)).kilometers
        address_distances[address] = distance

# Sort addresses by distance
sorted_addresses = sorted(address_distances.items(), key=lambda x: x[1])

# Print sorted addresses
for address, distance in sorted_addresses:
    print(f"{address}: {distance} km")
