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
    city = search[0]
    state = search[1].strip()
    country = search[2].strip()
    # raise Exception(city, state, country)
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city}
    response = requests.get(url, params=params).json()
    # return JsonResponse(response)
    if "results" not in response:
        return JsonResponse({"error": "City not found"}, status=404)
    else:
        filtered = [
            r for r in response["results"]
            if r.get("country") == country
            and r.get("admin1") == state
        ]
        response["results"] = filtered
    # return JsonResponse(response)
    lat = response["results"][0]["latitude"]
    lon = response["results"][0]["longitude"]

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
        icon = "clear.svg"
    elif 1 <= code <= 3:
        condition = "Cloudy"
        icon = "cloudy.svg"     # done
    elif 45 <= code <= 48:
        condition = "Mist / Fog"
        icon = "mist.svg"
    elif 51 <= code <= 57:
        condition = "Drizzle"
        icon = "drizzle.svg"
    elif 61 <= code <= 67:
        condition = "Rain"
        icon = "rain.svg"       # done
    elif 71 <= code <= 77:
        condition = "Snow"
        icon = "snow.svg"
    elif 80 <= code <= 82:
        condition = "Rain Showers"
        icon = "showers.svg"
    elif 85 <= code <= 86:
        condition = "Snow Showers"
        icon = "snow.svg"
    elif 95 <= code <= 99:
        condition = "Thunderstorm"
        icon = "thunder.svg"
    else:
        condition = "Unknown"
        icon = "default.svg"

    
    return render(request, "index.html", {
        "weather": weather_data,
        "city": f"{city}, {state}, {country}",
        "condition": condition,
        "icon": icon
    })