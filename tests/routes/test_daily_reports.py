from unittest import TestCase
import unittest
from unittest.mock import patch, Mock
import csv
from flask import request, jsonify
import requests

import sys

sys.path.insert(0, '../../src')
from app import app
from app import app


class TestLoadDailyReports(TestCase):
    # def setUp(self):
    #     self.app = app.

    def test_load_data_success(self):
        f = open("./01-01-2021.csv", "rb")
        file = f.read()
        url = 'http://127.0.0.1:5000/daily_reports/data'
        r = requests.post(url, data=file, headers={"Content-Type": "text/csv"})
        f.close()
        self.assertEqual(r.status_code, 200)

    def test_query_data_success(self):
        url = 'http://127.0.0.1:5000/daily_reports/cases'
        body = {"return_type": "json",
                "date": "01/01/21",
                "types": ["Confirmed"],
                "locations":
                    [
                        {"Country/Region": "Albania"},
                        {"Country/Region": "Canada", "Province/State": "Ontario"},
                        {"Country/Region": "Australia", "Province/State": "Queensland",
                         "Combined_Key": "Australian Capital Territory, Australia"}
                    ]
                }
        r = requests.post(url, json=body, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()
