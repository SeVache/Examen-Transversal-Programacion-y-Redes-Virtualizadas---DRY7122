import requests
import urllib.parse


route_url = "https://graphhopper.com/api/1/route?"
key = "66f1c4a7-a1cf-4a93-9655-d3d386d75de2"  # Replace with your Graphhopper API key

def geocoding(location, key):
    while location == "":
        location = input("Ingresa la localización de nuevo: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        
        print(f"Geocoding API URL for {new_loc} (Location Type: {value})\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print(f"Geocode API status: {json_status}\nError message: {json_data['message']}")
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles disponibles de vehículos en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]  
    vehicle = input("Ingresa un perfil de vehículo que esté en la lista anterior: ")
    if vehicle == "salir" or vehicle == "s":
        break
    elif vehicle not in profile:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    loc1 = input("Localización de inicio: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocoding(loc1, key)
    loc2 = input("Destino: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print(f"Routing API Status: {paths_status}\nRouting API URL:\n{paths_url}")
        print("=================================================")
        print(f"Direcciones desde {orig[3]} hacia {dest[3]} en {vehicle}")
        print("=================================================")
        if paths_status == 200:
            miles = paths_data["paths"][0]["distance"] / 1000 / 1.61
            km = paths_data["paths"][0]["distance"] / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print(f"Distancia de viaje: {km:.2f} km")
            print(f"Distancia de viaje: {miles:.2f} millas")
            print(f"Duración del viaje: {hr:02d}:{min:02d}:{sec:02d}")
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print(f"{path} ({distance / 1000:.2f} km)({distance / 1000 / 1.61:.2f} millas)")
            print("=============================================")
        else:
            print(f"Mensaje de error: {paths_data['message']}")
            print("*******")