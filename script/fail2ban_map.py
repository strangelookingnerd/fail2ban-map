#!/usr/bin/python3

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
import os
import random
import sys
import requests

JSON_FILE = os.path.dirname(os.path.realpath(__file__)) + "/../public/places.geojson"
GEOIP_API = "http://ip-api.com/json/{}"
ADD_RANDOM_OFFSET = True


def find_lat_lng(ip_address: str) -> dict:
    """Fetches latitude and longitude for a given IP address using an external API."""
    point = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [0.0, 0.0]},
        "properties": {"name": ip_address, "place": "", "show_on_map": False},
    }

    try:
        response = requests.get(GEOIP_API.format(ip_address), timeout=5)
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
        print(f"Error fetching geolocation for {ip_address}: {ex}", file=sys.stderr)

    return point


def add(ip_address: str, json_file=JSON_FILE) -> None:
    """Adds a new IP geolocation point to the GeoJSON file."""
    new_point = find_lat_lng(ip_address)

    data = _load_json(json_file)

    replaced = False

    if data is None:
        data = {"type": "FeatureCollection", "features": []}
    else:
        for i, feature in enumerate(data["features"]):
            if feature["properties"]["name"] == ip_address:
                data["features"][i] = new_point
                replaced = True
                break

    if not replaced:
        data["features"].append(new_point)

    _save_json(data, json_file)


def remove(ip_address: str, json_file=JSON_FILE) -> None:
    """Removes an IP from the GeoJSON file."""

    data = _load_json(json_file)

    if data is not None:
        data["features"] = [feature for feature in data["features"] if feature["properties"]["name"] != ip_address]

        _save_json(data, json_file)


def _load_json(json_file=JSON_FILE) -> json:
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {json_file} not found.", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {json_file}.", file=sys.stderr)
        return None


def _save_json(data: str, json_file=JSON_FILE) -> None:
    try:
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    # pylint: disable=broad-exception-caught
    except Exception as ex:
        print(f"Error writing to {json_file}: {ex}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1].lower() == "add":
        add(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "remove":
        remove(sys.argv[2])
    else:
        print(f"Usage: {os.path.basename(sys.argv[0])} <COMMAND> <IP_ADDRESS>\n"
              f"The commands supported by {os.path.basename(sys.argv[0])} are:\n"
              f"    add     <IP_ADDRESS>     Adds a new IP geolocation point to the GeoJSON file.\n"
              f"    remove  <IP_ADDRESS>     Removes a IP geolocation point from the GeoJSON file.", file=sys.stderr)
