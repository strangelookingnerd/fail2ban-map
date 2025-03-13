#!/usr/bin/python3

import unittest
import json
import os
# pylint: disable=import-error
from public.fail2ban_map import find_lat_lng, add

class Test(unittest.TestCase):
    """Collection of tests for fail2ban_map."""
    def setUp(self):
        """Runs before each test."""
        self.test_ip = "8.8.8.8"  # Google's public DNS IP
        self.temp_json_file = "test_places.geojson"

        if os.path.exists(self.temp_json_file):
            os.remove(self.temp_json_file)

    def tearDown(self):
        """Runs after each test to clean up."""
        if os.path.exists(self.temp_json_file):
            os.remove(self.temp_json_file)

    def test_find_lat_lng_real(self):
        """Test if find_lat_lng() fetches real coordinates from API."""
        result = find_lat_lng(self.test_ip)

        self.assertIsInstance(result, dict)
        self.assertIn("geometry", result)
        self.assertIn("coordinates", result["geometry"])
        self.assertEqual(len(result["geometry"]["coordinates"]), 2)
        self.assertTrue(-180 <= result["geometry"]["coordinates"][0] <= 180)
        self.assertTrue(-90 <= result["geometry"]["coordinates"][1] <= 90)
        self.assertTrue(result["properties"]["show_on_map"])

    def test_add_function_real(self):
        """Test if add() correctly appends data to the GeoJSON file."""
        add(self.test_ip, json_file=self.temp_json_file)

        self.assertTrue(os.path.exists(self.temp_json_file))

        with open(self.temp_json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertIn("features", data)
        self.assertGreater(len(data["features"]), 0)

        last_entry = data["features"][-1]
        self.assertEqual(last_entry["properties"]["name"], self.test_ip)

if __name__ == "__main__":
    unittest.main()
