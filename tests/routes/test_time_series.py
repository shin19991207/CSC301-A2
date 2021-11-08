from unittest import TestCase
import requests


class TestLoadTimeSeries(TestCase):
    def test_load_data_success(self):
        f = open("./time_series_covid19_recovered_global.csv", "rb")
        file = f.read()
        url = 'http://127.0.0.1:5000/time_series/data?type=recovered'
        r = requests.post(url, data=file, headers={"Content-Type": "text/csv"})
        f.close()
        print(r)
