# from flask import Blueprint, request, jsonify
# from datetime import datetime, timedelta
# import requests

# weather_sd = Blueprint('weather_sd', __name__,url_prefix="/weather")

# from flask import request, jsonify
# import requests
# from datetime import datetime, timedelta
# # from Weather_details.config import API_KEY  # Your config file where API_KEY is stored

# @weather_sd.route('/weather_details', methods=['POST'])
# def weather_details():
#     data = request.get_json()
    
#     taluka_type = data.get('taluka_type')
#     prediction_days = data.get('prediction_days')

#     # Get today's date
#     today = datetime.today().date()

#     print(f"Received Weather Details:")
#     print(f"Taluka Type: {taluka_type}")
#     print(f"Prediction Period (days): {prediction_days}")
#     print(f"Today's Date: {today}")

#     # 1. First get the lat/lon of the Taluka using Open-Meteo Geocoding
#     geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={taluka_type}&count=1&language=en&format=json"
#     location_response = requests.get(geocoding_url)
#     location_data = location_response.json()
#     print(location_data,"location data")
#     if 'results' not in location_data or not location_data['results']:
#         return jsonify({"error": "Location not found!"}), 404

#     lat = location_data['results'][0]['latitude']
#     lon = location_data['results'][0]['longitude']
    
#     print(lat, lon,"......................lat,lon.............................")
#     lat = 16.2655
#     lon = 73.7083
#     # 2. Prepare start and end dates
#     start_date = today
#     end_date = today + timedelta(days=prediction_days - 1)

#     # 3. Fetch Weather Forecast from Open-Meteo
#     weather_url = (
#         f"https://api.open-meteo.com/v1/forecast?"
#         f"latitude={lat}&longitude={lon}"
#         f"&start_date={start_date}&end_date={end_date}"
#         f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
#         f"&timezone=auto"
#     )

#     weather_response = requests.get(weather_url)
#     weather_data = weather_response.json()

#     if 'daily' not in weather_data:
#         return jsonify({"error": "Weather forecast not available!"}), 404

#     # 4. Prepare Forecast
#     forecast = []
#     daily_data = weather_data['daily']

#     for i in range(len(daily_data['time'])):
#         day_info = {
#             "date": daily_data['time'][i],
#             "temperature_max": daily_data['temperature_2m_max'][i],
#             "temperature_min": daily_data['temperature_2m_min'][i],
#             "precipitation_sum": daily_data['precipitation_sum'][i],
#             "wind_speed_max": daily_data['wind_speed_10m_max'][i]
#         }
#         forecast.append(day_info)
#         print(forecast,".................forecast......................")

#     return jsonify({
#         "talukaType": taluka_type,
#         "predictionDays": prediction_days,
#         "today": today.strftime("%Y-%m-%d"),
#         "forecast": forecast
#     })

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import requests

weather_sd = Blueprint('weather_sd', __name__, url_prefix="/weather")

from flask import request, jsonify
import requests
from datetime import datetime, timedelta
# from Weather_details.config import API_KEY  # Your config file where API_KEY is stored

@weather_sd.route('/weather_details', methods=['POST'])
def weather_details():
    data = request.get_json()
    
    taluka_type = data.get('talukaType')
    crop_type = data.get('cropType')
    tree_age = data.get('treeAge')
    prediction_days = data.get('predictionDays')

    # Get today's date
    today = datetime.today().date()

    print(f"Received Weather Details:")
    print(f"Taluka Type: {taluka_type}")
    print(f"Crop Type: {crop_type}")
    print(f"Tree Age (years): {tree_age}")
    print(f"Prediction Period (days): {prediction_days}")
    print(f"Today's Date: {today}")

    # 1. First get the lat/lon of the Taluka using Open-Meteo Geocoding
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={taluka_type}&count=1&language=en&format=json"
    location_response = requests.get(geocoding_url)
    location_data = location_response.json()

    if 'results' not in location_data or not location_data['results']:
        return jsonify({"error": "Location not found!"}), 404

    lat = location_data['results'][0]['latitude']
    lon = location_data['results'][0]['longitude']
    
    print(lat, lon,"......................lat,lon.............................")

    # 2. Prepare start and end dates
    start_date = today
    end_date = today + timedelta(days=prediction_days - 1)

    # 3. Fetch Weather Forecast from Open-Meteo
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"
        f"&timezone=auto"
    )

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if 'daily' not in weather_data:
        return jsonify({"error": "Weather forecast not available!"}), 404

    # 4. Prepare Forecast
    forecast = []
    daily_data = weather_data['daily']

    for i in range(len(daily_data['time'])):
        day_info = {
            "date": daily_data['time'][i],
            "temperature_max": daily_data['temperature_2m_max'][i],
            "temperature_min": daily_data['temperature_2m_min'][i],
            "precipitation_sum": daily_data['precipitation_sum'][i],
            "wind_speed_max": daily_data['wind_speed_10m_max'][i]
        }
        forecast.append(day_info)
        print(forecast,".................forecast......................")

    return jsonify({
        "talukaType": taluka_type,
        "cropType": crop_type,
        "treeAge": tree_age,
        "predictionDays": prediction_days,
        "today": today.strftime("%Y-%m-%d"),
        "forecast": forecast
    })
