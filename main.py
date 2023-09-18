from audioop import avg
import os
import folium
import requests
import json

r = requests.get(url="https://api.covid19india.org/data.json")
statewise_covid_data = json.loads(r.content)["statewise"]

with open("capital_data.json", "r") as f:
    json_text= f.read()

city_data = json.loads(json_text)


for i in range(1, len(statewise_covid_data)):
    for j in range(len(city_data)):
        if statewise_covid_data[i]["statecode"] == city_data[j]["statecode"]:
            city_data[j]["confirmed"] = statewise_covid_data[i]["confirmed"]
            city_data[j]["active"] = statewise_covid_data[i]["active"]
            break


mp = folium.Map(location=[city_data[1]["lat"], city_data[1]["lng"]], zoom_start=5)

# average active cases
avg_active_cases = 0
total_active = 0

for i in range(len(city_data)):
    if "active" not in city_data[i]:
        continue
    total_active += int(city_data[i]["active"])
    avg_active_cases =total_active // len(city_data)

for i in range(len(city_data)):
    if "active" not in city_data[i]:
        continue

    active = city_data[i]["active"]
    lat = city_data[i]["lat"]
    long = city_data[i]["lng"]
    tooltip = "active: " + active + " confirmed: " + city_data[i]["confirmed"]

    if int(active) > avg_active_cases:
        folium.Marker(
            location=[lat, long],
            popup=city_data[i]["state"],
            icon=folium.Icon(
                color="darkred",
                icon_color="white",
                icon="remove-sign",
            ),
            tooltip=tooltip,
        ).add_to(mp)
    elif int(active) > avg_active_cases / 2:
        folium.Marker(
            location=[lat, long],
            popup=city_data[i]["state"],
            icon=folium.Icon(
                color="red",
                icon_color="white",
                icon="ban-circle",
            ),
            tooltip=tooltip,
        ).add_to(mp)
    elif int(active) > avg_active_cases / 4:
        folium.Marker(
            location=[lat, long],
            popup=city_data[i]["state"],
            icon=folium.Icon(
                color="orange",
                icon_color="white",
                icon="warning-sign",
            ),
            tooltip=tooltip,
        ).add_to(mp)

    else:
        folium.Marker(
            location=[lat, long],
            popup=city_data[i]["state"],
            icon=folium.Icon(
                color="green",
                icon_color="white",
                icon="ok-circle",
            ),
            tooltip=tooltip,
        ).add_to(mp)

mp.save("index.html")

# os.system("google-chrome index.html &")
