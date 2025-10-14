#!/usr/bin/python3
import os
import runpy
import sys
# pylint: disable=import-error
from script import fail2ban_map
# pylint: disable=import-error
from script.fail2ban_map import find_lat_lng, add, remove, _load_json, _save_json

TEST_IP_1 = "8.8.8.8"  # Google's public DNS IP
TEST_IP_2 = "8.8.4.4"  # Google's public DNS IP
TEMP_JSON_FILE = "test_places.geojson"


# pylint: disable=unused-argument
def setup_function(function):
    """Runs before each test."""
    if os.path.exists(TEMP_JSON_FILE):
        os.remove(TEMP_JSON_FILE)


# pylint: disable=unused-argument
def teardown_function(function):
    """Runs after each test to clean up."""
    if os.path.exists(TEMP_JSON_FILE):
        os.remove(TEMP_JSON_FILE)


def test_load_json_invalid_json(capsys):
    """Test _load_json() fails gracefully."""
    with open(TEMP_JSON_FILE, "w", encoding="utf-8") as file:
        file.write("{ invalid json }")
    result = _load_json(TEMP_JSON_FILE)

    assert result is None
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Error decoding JSON from test_places.geojson." in captured.err


def test_save_json_invalid_file(capsys):
    """Test _save_json() fails gracefully."""
    folder = "folder"
    os.makedirs(folder, exist_ok=True)
    _save_json("{}", folder)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"Error writing to {folder}:" in captured.err

    assert os.path.isdir(folder)
    os.removedirs(folder)


def test_find_lat_lng():
    """Test find_lat_lng() fetches real coordinates from API."""
    result = find_lat_lng(TEST_IP_1)

    assert isinstance(result, dict)
    assert "geometry" in result
    assert "coordinates" in result["geometry"]
    assert len(result["geometry"]["coordinates"]) == 2
    assert -180 <= result["geometry"]["coordinates"][0] <= 180
    assert -90 <= result["geometry"]["coordinates"][1] <= 90
    assert result["properties"]["show_on_map"]


def test_find_lat_lng_bad_ip(capsys):
    """Test find_lat_lng() fails gracefully."""
    result = find_lat_lng("this_is_no_ip")

    assert isinstance(result, dict)
    assert "geometry" in result
    assert "coordinates" in result["geometry"]
    assert len(result["geometry"]["coordinates"]) == 2
    assert result["geometry"]["coordinates"][0] == 0
    assert result["geometry"]["coordinates"][1] == 0
    assert not result["properties"]["show_on_map"]

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_find_lat_lng_bad_request(capsys):
    """Test find_lat_lng() fails gracefully."""
    # switch out the api
    api = fail2ban_map.GEOIP_API
    fail2ban_map.GEOIP_API = "https//doesnotexist.com/{}"

    result = find_lat_lng(TEST_IP_1)

    assert isinstance(result, dict)
    assert "geometry" in result
    assert "coordinates" in result["geometry"]
    assert len(result["geometry"]["coordinates"]) == 2
    assert result["geometry"]["coordinates"][0] == 0
    assert result["geometry"]["coordinates"][1] == 0
    assert not result["properties"]["show_on_map"]

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"Error fetching geolocation for {TEST_IP_1}:" in captured.err

    # switch back
    fail2ban_map.GEOIP_API = api


def test_add(capsys):
    """add() correctly appends data to the GeoJSON file."""
    add(TEST_IP_1, json_file=TEMP_JSON_FILE)
    add(TEST_IP_2, json_file=TEMP_JSON_FILE)

    assert os.path.exists(TEMP_JSON_FILE)

    data = _load_json(json_file=TEMP_JSON_FILE)

    assert "features" in data
    assert len(data["features"]) == 2

    entry = data["features"][-2]
    assert entry["properties"]["name"] == TEST_IP_1

    entry = data["features"][-1]
    assert entry["properties"]["name"] == TEST_IP_2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"File {TEMP_JSON_FILE} not found." in captured.err


def test_add_replacement(capsys):
    """add() correctly replaces data in the GeoJSON file."""
    add(TEST_IP_1, json_file=TEMP_JSON_FILE)
    add(TEST_IP_2, json_file=TEMP_JSON_FILE)
    add(TEST_IP_1, json_file=TEMP_JSON_FILE)  # add again

    assert os.path.exists(TEMP_JSON_FILE)

    data = _load_json(json_file=TEMP_JSON_FILE)

    assert "features" in data
    assert len(data["features"]) == 2

    entry = data["features"][-2]
    assert entry["properties"]["name"] == TEST_IP_1

    entry = data["features"][-1]
    assert entry["properties"]["name"] == TEST_IP_2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"File {TEMP_JSON_FILE} not found." in captured.err


def test_remove(capsys):
    """remove() correctly removes data from the GeoJSON file."""
    add(TEST_IP_1, json_file=TEMP_JSON_FILE)
    add(TEST_IP_2, json_file=TEMP_JSON_FILE)

    assert os.path.exists(TEMP_JSON_FILE)

    remove(TEST_IP_1, json_file=TEMP_JSON_FILE)

    data = _load_json(json_file=TEMP_JSON_FILE)

    assert "features" in data
    assert len(data["features"]) == 1

    entry = data["features"][-1]
    assert entry["properties"]["name"] == TEST_IP_2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"File {TEMP_JSON_FILE} not found." in captured.err


def test_remove_non_existent(capsys):
    """remove() does not remove valid data from the GeoJSON file."""
    add(TEST_IP_1, json_file=TEMP_JSON_FILE)

    assert os.path.exists(TEMP_JSON_FILE)

    remove("127.0.0.1", json_file=TEMP_JSON_FILE)

    data = _load_json(json_file=TEMP_JSON_FILE)

    assert "features" in data
    assert len(data["features"]) == 1

    entry = data["features"][-1]
    assert entry["properties"]["name"] == TEST_IP_1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert f"File {TEMP_JSON_FILE} not found." in captured.err


def test_main(capsys):
    """main() prints output as expected."""
    sys.argv = [fail2ban_map, "add", "1.2.3.4"]
    runpy.run_path("script/fail2ban_map.py", run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    sys.argv = [fail2ban_map, "remove", "1.2.3.4"]
    runpy.run_path("script/fail2ban_map.py", run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

    sys.argv = [fail2ban_map, "derp", "1.2.3.4"]
    runpy.run_path("script/fail2ban_map.py", run_name="__main__")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Usage: fail2ban_map.py <COMMAND> <IP_ADDRESS>" in captured.err
