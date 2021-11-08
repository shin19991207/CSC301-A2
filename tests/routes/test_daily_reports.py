from unittest import TestCase
from unittest.mock import patch, Mock
import csv
from flask import request
import requests


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
