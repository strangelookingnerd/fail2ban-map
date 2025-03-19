#!/usr/bin/python3

import unittest
import os
# pylint: disable=import-error
from script.fail2ban_map import find_lat_lng, add, remove, _load_json


class Test(unittest.TestCase):
    """Collection of tests for fail2ban_map."""
    def setUp(self):
        """Runs before each test."""
        self.test_ip_1 = "8.8.8.8"  # Google's public DNS IP
        self.test_ip_2 = "8.8.4.4"  # Google's public DNS IP
        self.temp_json_file = "test_places.geojson"

        if os.path.exists(self.temp_json_file):
            os.remove(self.temp_json_file)

    def tearDown(self):
        """Runs after each test to clean up."""
        if os.path.exists(self.temp_json_file):
            os.remove(self.temp_json_file)

    def test_find_lat_lng(self):
        """Test find_lat_lng() fetches real coordinates from API."""
        result = find_lat_lng(self.test_ip_1)

        self.assertIsInstance(result, dict)
        self.assertIn("geometry", result)
        self.assertIn("coordinates", result["geometry"])
        self.assertEqual(len(result["geometry"]["coordinates"]), 2)
        self.assertTrue(-180 <= result["geometry"]["coordinates"][0] <= 180)
        self.assertTrue(-90 <= result["geometry"]["coordinates"][1] <= 90)
        self.assertTrue(result["properties"]["show_on_map"])

    def test_add(self):
        """add() correctly appends data to the GeoJSON file."""
        add(self.test_ip_1, json_file=self.temp_json_file)
        add(self.test_ip_2, json_file=self.temp_json_file)

        self.assertTrue(os.path.exists(self.temp_json_file))

        data = _load_json(json_file=self.temp_json_file)

        self.assertIn("features", data)
        self.assertEqual(len(data["features"]), 2)

        entry = data["features"][-2]
        self.assertEqual(entry["properties"]["name"], self.test_ip_1)

        entry = data["features"][-1]
        self.assertEqual(entry["properties"]["name"], self.test_ip_2)

    def test_add_replacement(self):
        """add() correctly replaces data in the GeoJSON file."""
        add(self.test_ip_1, json_file=self.temp_json_file)
        add(self.test_ip_2, json_file=self.temp_json_file)
        add(self.test_ip_1, json_file=self.temp_json_file) # add again

        self.assertTrue(os.path.exists(self.temp_json_file))

        data = _load_json(json_file=self.temp_json_file)

        self.assertIn("features", data)
        self.assertEqual(len(data["features"]), 2)

        entry = data["features"][-2]
        self.assertEqual(entry["properties"]["name"], self.test_ip_1)

        entry = data["features"][-1]
        self.assertEqual(entry["properties"]["name"], self.test_ip_2)

    def test_remove(self):
        """remove() correctly removes data from the GeoJSON file."""
        add(self.test_ip_1, json_file=self.temp_json_file)
        add(self.test_ip_2, json_file=self.temp_json_file)

        self.assertTrue(os.path.exists(self.temp_json_file))

        remove(self.test_ip_1, json_file=self.temp_json_file)

        data = _load_json(json_file=self.temp_json_file)

        self.assertIn("features", data)
        self.assertEqual(len(data["features"]), 1)

        entry = data["features"][-1]
        self.assertEqual(entry["properties"]["name"], self.test_ip_2)

    def test_remove_non_existent(self):
        """remove() does not remove valid data from the GeoJSON file."""
        add(self.test_ip_1, json_file=self.temp_json_file)

        self.assertTrue(os.path.exists(self.temp_json_file))

        remove("127.0.0.1", json_file=self.temp_json_file)

        data = _load_json(json_file=self.temp_json_file)

        self.assertIn("features", data)
        self.assertEqual(len(data["features"]), 1)

        entry = data["features"][-1]
        self.assertEqual(entry["properties"]["name"], self.test_ip_1)

if __name__ == "__main__":
    unittest.main()
