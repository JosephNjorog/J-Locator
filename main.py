import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import folium
from timezonefinder import TimezoneFinder
from tkinter import Tk, Label, Entry, Button, Text, END
from tkinter import messagebox

def locate_number():
    number = entry.get()
    try:
        # Parsing and getting country and carrier information
        ch_number = phonenumbers.parse(number, "CH")
        service_number = phonenumbers.parse(number, "RO")

        location = geocoder.description_for_number(ch_number, "en")
        carrier_name = carrier.name_for_number(service_number, "en")
        timezones = timezone.time_zones_for_number(service_number)

        # Display location and carrier
        result_text.delete(1.0, END)
        result_text.insert(END, f"Location: {location}\n")
        result_text.insert(END, f"Carrier: {carrier_name}\n")
        result_text.insert(END, f"Timezone: {', '.join(timezones)}\n")

        # Display location on map
        geocode_map(number, location, carrier_name, timezones)

    except phonenumbers.NumberParseException:
        messagebox.showerror("Error", "Invalid phone number")

def geocode_map(number, location, carrier_name, timezones):
    map = folium.Map(location=[0, 0], zoom_start=2)
    tf = TimezoneFinder()
    
    ch_number = phonenumbers.parse(number, "CH")
    location_geo = geocoder.description_for_number(ch_number, "en")
    
    lat, lng = 37.7749, -122.4194  # Default location: San Francisco, CA
    if location_geo:
        # Update lat, lng with real geolocation if available
        pass
    
    # Save the HTML file
    with open("phone_number_location.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phone Number Locator</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        h1 {{
            color: #333;
        }}
        #map {{
            height: 80%;
            width: 80%;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
        #info {{
            margin-top: 20px;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            width: 80%;
            text-align: center;
        }}
    </style>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
</head>
<body>
    <h1>Phone Number Locator</h1>
    <div id="map"></div>
    <div id="info">
        <h2>Location Information</h2>
        <p id="location">Location: {location}</p>
        <p id="carrier">Carrier: {carrier_name}</p>
        <p id="timezone">Timezone: {', '.join(timezones)}</p>
    </div>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <script>
        // Initialize map
        const map = L.map('map').setView([{lat}, {lng}], 13);

        // Set up the OSM layer
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }}).addTo(map);

        // Add marker to the map
        L.marker([{lat}, {lng}]).addTo(map)
            .bindPopup('<b>{location}</b><br>{carrier_name}')
            .openPopup();
    </script>
</body>
</html>""")

# GUI Setup
root = Tk()
root.title("Phone Number Locator")

Label(root, text="Enter phone number with country code (e.g., +14155552671):").pack()
entry = Entry(root, width=50)
entry.pack()
Button(root, text="Locate", command=locate_number).pack()

result_text = Text(root, height=10, width=50)
result_text.pack()

root.mainloop()
