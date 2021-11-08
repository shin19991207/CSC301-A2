from unittest import TestCase
import unittest
import requests

# import sys
#
# sys.path.insert(0, '../../src')


class TestLoadTimeSeries(TestCase):
    def test_load_data_success(self):
        f = open("tests/routes/time_series_covid19_recovered_global.csv", "rb")
        file = f.read()
        url = 'https://covid-monitor-61.herokuapp.com/time_series/data?type=recovered'
        r = requests.post(url, data=file, headers={"Content-Type": "text/csv"})
        f.close()
        self.assertEqual(r.status_code, 200)

    def test_query_data(self):
        url = 'https://covid-monitor-61.herokuapp.com/time_series/cases'
        body = {"return_type": "json",
                "start_date": "01/26/20",
                "end_date": "01/28/20",
                "types": ["Recovered"],
                "locations":
                    [
                        {"Country/Region": "Albania"},
                        {"Country/Region": "Canada", "Province/State": "Ontario"},
                        {"Country/Region": "Australia"}
                    ]
                }
        r = requests.post(url, json=body, headers={"Content-Type": "application/json"})
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
