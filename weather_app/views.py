from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse

# Create your views here.

def index(request):
    # return HttpResponse("Weather App")
    return render(request, "index.html")

def get_coordinates(request):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    # params = {"name": city}
    params = {"name": "bilaspur"}
    response = requests.get(url, params=params).json()

    # if "results" not in response:
    #     return JsonResponse({"error": "City not found"}, status=404)

    # lat = response["results"][0]["latitude"]
    # lon = response["results"][0]["longitude"]

    # return JsonResponse({"city": city, "latitude": lat, "longitude": lon})
    
    return JsonResponse(response)

def weather(request):
    search = request.POST.get("city").split(",")
    # raise Exception(search)
     
    if len(search) >= 1:
        city = search[0].strip()
    else:
        return JsonResponse({"error": "Invalid city input"}, status=400)
    
    state = search[1].strip() if len(search) >= 2 else None
    country = search[2].strip() if len(search) == 3 else None
    
    # raise Exception(city, state, country)

    # ---------- GEO CODING ----------
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city}
    response = requests.get(url, params=params).json()
    # return JsonResponse(response)
    if "results" not in response or not response["results"]:
        return JsonResponse({"error": "City not found"}, status=404)

    results = response["results"]
    # filtering only when data exists
    if country:
        results = [
            r for r in results
            if r.get("country", "").lower() == country.lower()
        ]

    if state:
        results = [
            r for r in results
            if r.get("admin1", "").lower() == state.lower()
        ]

    if not results:
        return JsonResponse({"error": "No matching location found"}, status=404)

    response["results"] = results
    
    # return JsonResponse(response)
    weather_list = []
    for res in response["results"]:
        lat = res["latitude"]
        lon = res["longitude"]

        # ---------- WEATHER ----------
        weather_data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True}
        ).json()

    # {
    #     # "latitude": 22.125,
    #     # "longitude": 82.125,
    #     "generationtime_ms": 0.0665187835693359,
    #     "utc_offset_seconds": 0,
    #     # "timezone": "GMT",
    #     "timezone_abbreviation": "GMT",
    #     "elevation": 262,
    #     "current_weather_units": {
    #         "time": "iso8601",
    #         "interval": "seconds",
    #         "temperature": "°C",
    #         "windspeed": "km/h",
    #         "winddirection": "°",
    #         "is_day": "",
    #         "weathercode": "wmo code"
    #     },
    #     "current_weather": {
    #         # "time": "2025-12-22T10:15",
    #         "interval": 900,
    #         # "temperature": 24,
    #         # "windspeed": 2.1,
    #         # "winddirection": 121,
    #         "is_day": 1,
    #         # "weathercode": 0
    #     }
    # }
    # return JsonResponse(weather)
        code = weather_data["current_weather"]["weathercode"]

        if code == 0:
            condition = "Clear Sky"
            icon = "images/we/Clear_sky.png"
        elif 1 <= code <= 3:
            condition = "Cloudy"
            icon = "images/we/cloudy.png"
        elif 45 <= code <= 48:
            condition = "Mist / Fog"
            icon = "images/we/mist_fog.png"
        elif 51 <= code <= 57:
            condition = "Drizzle"
            icon = "images/we/drizzle.png"
        elif 61 <= code <= 67:
            condition = "Rain"
            icon = "images/we/cloud-rain.svg"
        elif 71 <= code <= 77:
            condition = "Snow"
            icon = "images/we/snow.svg"
        elif 80 <= code <= 82:
            condition = "Rain Showers"
            icon = "images/we/weather-rain-showers-day.svg"
        elif 85 <= code <= 86:
            condition = "Snow Showers"
            icon = "images/we/snow.svg"
        elif 95 <= code <= 99:
            condition = "Thunderstorm"
            icon = "images/we/thunderstrom.png"
        else:
            condition = "Unknown"
            icon = "images/default.svg"

        weather_list.append({
            "city": res.get("name"),
            "state": res.get("admin1"),
            "country": res.get("country"),
            "location": f'{res.get("name")}, {res.get("admin1")}, {res.get("country")}',
            "latitude": lat,
            "longitude": lon,
            "temperature": weather_data["current_weather"]["temperature"],
            "windspeed": weather_data["current_weather"]["windspeed"],
            "weathercode": code,
            "condition": condition,
            "icon": icon,
            "time": weather_data["current_weather"]["time"],
            "direction": weather_data["current_weather"]["winddirection"],
        })

    return render(request, "index.html", {"weather_list": weather_list})