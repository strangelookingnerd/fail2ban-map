# MIT License
#
# Copyright (c) 2025 strangelookingnerd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import random
import sys
import requests

JSON_FILE = "places.geojson"
GEOIP_API = "http://ip-api.com/json/{}"
ADD_RANDOM_OFFSET = True


def find_lat_lng(ipaddr: str) -> dict:
    """Fetches latitude and longitude for a given IP address using an external API."""
    point = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [0.0, 0.0]},
        "properties": {"name": ipaddr, "place": "", "show_on_map": False},
    }

    try:
        response = requests.get(GEOIP_API.format(ipaddr), timeout=5)
        response.raise_for_status()
        geo_value = response.json()

        if "lon" in geo_value and "lat" in geo_value:
            point["geometry"]["coordinates"] = [float(geo_value["lon"]), float(geo_value["lat"])]
            point["properties"]["place"] = f"{geo_value.get('city', 'Unknown')}, {geo_value.get('country', 'Unknown')}"
            point["properties"]["show_on_map"] = True

            if ADD_RANDOM_OFFSET:
                point["geometry"]["coordinates"][0] += random.uniform(-0.01, 0.01)
                point["geometry"]["coordinates"][1] += random.uniform(-0.01, 0.01)

    except requests.RequestException as ex:
        print(f"Error fetching geolocation for {ipaddr}: {ex}", file=sys.stderr)

    return point


def add(ipaddr: str, json_file=JSON_FILE) -> None:
    """Adds a new IP geolocation point to the GeoJSON file."""
    new_point = find_lat_lng(ipaddr)

    # Load existing data
    data = {"type": "FeatureCollection", "features": []}
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {json_file} not found. Creating a new one.", file=sys.stderr)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {json_file}. Using an empty dataset.", file=sys.stderr)

    # Append new point and write back
    data["features"].append(new_point)

    try:
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except Exception as ex:
        print(f"Error writing to {json_file}: {ex}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <IP_ADDRESS>", file=sys.stderr)
        sys.exit(1)

    add(sys.argv[1])
