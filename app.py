from flask import Flask, request, render_template
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import folium

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

def get_detailed_location(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    result = response.json()
    if result['status'] == 'OK':
        return result['results'][0]
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    location = ''
    carrier_name = ''
    timezones = ''
    map_html = ''
    detailed_location_info = ''

    if request.method == 'POST':
        number = request.form.get('number')
        try:
            ch_number = phonenumbers.parse(number, "CH")
            service_number = phonenumbers.parse(number, "RO")

            location = geocoder.description_for_number(ch_number, "en")
            carrier_name = carrier.name_for_number(service_number, "en")
            timezones = ', '.join(timezone.time_zones_for_number(service_number))

            # Get detailed location info
            address = f"{location}"
            location_info = get_detailed_location(address)
            if location_info:
                detailed_location_info = location_info.get('formatted_address', 'Address not found')

            # Generate map
            map = folium.Map(location=[37.7749, -122.4194], zoom_start=13)  # Default location
            folium.Marker([37.7749, -122.4194], popup=f'<b>{location}</b><br>{carrier_name}').add_to(map)

            # Convert map to HTML
            map_html = map._repr_html_()

        except phonenumbers.NumberParseException:
            location = "Invalid phone number"

    return render_template('phone_number_locator.html',
                            location=location, 
                            carrier_name=carrier_name, 
                            timezones=timezones, 
                            map_html=map_html, 
                            detailed_location_info=detailed_location_info)

if __name__ == '__main__':
    app.run(debug=True)
