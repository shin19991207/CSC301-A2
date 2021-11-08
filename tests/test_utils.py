import sys
import unittest
import psycopg2

sys.path.insert(0, '../src')

from src.utils import daily_reports_return_json, daily_reports_return_csv, time_series_return_csv, check_query_data_active, check_request
from src.config import connect_database
# import copy


class TestUtils(unittest.TestCase):
    def test_daily_reports_return_json(self):
        try:
            conn = connect_database()
            cur = conn.cursor()
            # create a test table in the database with the table format of a daily report
            cur.execute("DROP TABLE IF EXISTS test;")
            conn.commit()
            cur.execute("CREATE TABLE test (state VARCHAR(5), region VARCHAR(5), last_update VARCHAR(20), "
                        "confirmed INTEGER, deaths INTEGER, recovered INTEGER, active INTEGER, combined_key VARCHAR("
                        "5));")
            conn.commit()
            cur.execute("INSERT INTO test VALUES ('a', 'a', '2021-01-02 05:22:33', 10, 5, 0, 5, 'a, a'), "
                        "(null, 'b', '2021-01-02 05:22:33', 1, 0, 0, 1, 'b'), "
                        "('b', 'b', '2021-01-02 05:22:33', 4, 3, 0, 1, 'b, b');"
                        )
            conn.commit()

            date = "01/01/21"
            types = ["Confirmed", "Deaths", "Recovered", "Active"]
            locations = [{"Country/Region": "b"},
                         {"Country/Region": "a", "Province/State": "a", "Combined_Key": "a, a"}
                         ]
            result = daily_reports_return_json(cur, date, locations, types, 'test')

            expected = {
                "Date": date,
                "Reports": [
                    {
                        "Active": 2,
                        "Confirmed": 5,
                        "Country/Region": "b",
                        "Deaths": 3,
                        "Recovered": 0
                    },
                    {
                        "Active": 5,
                        "Confirmed": 10,
                        "Country/Region": "a",
                        "Deaths": 5,
                        "Province/State": "a",
                        "Combined_Key": "a, a",
                        "Recovered": 0
                    }
                ]
            }
            self.assertEqual(result, expected)

        except psycopg2.Error:
            pass

    def test_daily_reports_return_csv(self):
        json_data = {
            "Date": "01/01/21",
            "Reports": [
                {
                    "Active": 2,
                    "Confirmed": 5,
                    "Country/Region": "b",
                    "Deaths": 3,
                    "Recovered": 0
                },
                {
                    "Active": 5,
                    "Confirmed": 10,
                    "Country/Region": "a",
                    "Deaths": 5,
                    "Province/State": "a",
                    "Combined_Key": "a, a",
                    "Recovered": 0
                }
            ]
        }
        result = daily_reports_return_csv(json_data, ["Confirmed", "Deaths", "Recovered", "Active"])
        expected = "Date,Province/State,Country/Region,Combined_Key,Confirmed,Deaths,Recovered,Active" \
                   "\n01/01/21,,b,,5,3,0,2\n01/01/21,a,a,a, a,10,5,0,5"
        self.assertEqual(result, expected)

    def test_time_series_return_csv(self):
        json_data = {"01/26/20": [{"Active": 0, "Confirmed": 0, "Country/Region": "Albania"}]}
        expected = "Date,Province/State,Country/Region,Confirmed\n01/26/20,,Albania,0"
        result = time_series_return_csv(json_data, ["01/26/20"], ["Confirmed"])
        self.assertEqual(result, expected)

    def test_check_query_data_active(self):
        conn = connect_database()
        cur = conn.cursor()
        # create a test table in the database with the table format of a daily report
        cur.execute("DROP TABLE IF EXISTS test;")
        conn.commit()
        self.assertEqual(check_query_data_active(cur, ["test"]), False)

    def test_check_request(self):
        result = check_request(['test'], {})
        self.assertEqual(result[0], 'test')


if __name__ == '__main__':
    unittest.main()
