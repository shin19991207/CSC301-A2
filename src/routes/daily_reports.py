from flask import Blueprint, request, jsonify, make_response
import psycopg2
from io import StringIO
from datetime import datetime, timedelta
import pandas as pd
from config import connect_database
from utils.daily_reports_util import return_json, return_csv
from utils.util import fail, check_request

daily_reports = Blueprint('daily_reports', __name__)

hard_column = ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed',
               'Deaths', 'Recovered', 'Active', 'Combined_Key', 'Incident_Rate', 'Case_Fatality_Ratio']


@daily_reports.route("/data", methods=['POST'])
def load_data():
    # check the format and type parameter
    if not request.content_type.startswith('text/csv'):
        return fail(400, "content type is not correct", "please check if your file is a csv file")

    data_content = request.data.decode('utf-8')
    buffer = StringIO()
    buffer.write(data_content)
    buffer.seek(0)
    zero_row = buffer.readline().strip().split(',')
    buffer.seek(0)
    csv_file = pd.read_csv(buffer)

    # check altitude and longitude
    Lat = csv_file['Lat']
    Long = csv_file['Long_']
    # check the data type
    if Lat.dtypes == "object" or Long.dtypes == "object":
        return fail(400, "datatype error in Lat and Long column",
                    "Latitude and Longitude should be floats or integers and nothing else")
    # check the range of latitude and longitude
    if Lat.max() > 90 or Lat.min() < -90 or Long.max() > 180 or Long.max() < -180:
        return fail(400, "error occur in Lat and Long column in the file ",
                    "Latitudes range from -90 to 90 inclusively, and longitudes range from -180 to 80"
                    " inclusively")

    # check the column of the upcoming files
    if zero_row != hard_column:
        return fail(400, "the content of the upcoming file does not meet expectation",
                    f"please check if your file miss a column suggested in the link:"
                    f"https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv")

    # check the datatype of Confirmed,Deaths,Recovered,Active
    # check_integer()
    types = csv_file.iloc[:, 7:11].dtypes
    for index, value in types.items():
        if not (value == "int64" or value == "float64"):
            return fail(400, "the content of the upcoming file does not meet expectation",
                        "numbers of people should be integers")

    conn = connect_database()
    cur = conn.cursor()
    cur.execute(f'drop table if exists daily_reports')
    conn.commit()
    create = 'create table daily_reports (state VARCHAR(100), region VARCHAR(100), last_update VARCHAR(100), ' \
             'confirmed integer, deaths integer, recovered integer, active integer, combined_key VARCHAR(100))'
    cur.execute(create)
    conn.commit()
    for i in range(len(csv_file)):
        modified_state = str(csv_file.iloc[i, 2]).replace("'", "''")
        modified_region = str(csv_file.iloc[i, 3]).replace("'", "''")
        modified_combined = str(csv_file.iloc[i, 11]).replace("'", "''")
        people = ','.join(csv_file.iloc[i, 7:11].apply(str).values)
        insertion_str = f"'{modified_state}', '{modified_region}', '{csv_file.iloc[i, 4]}', {people.replace('nan', 'null')}, '{modified_combined}'"
        insertion = f'insert into daily_reports (state, region, last_update, confirmed, deaths, recovered, ' \
                    f'active, combined_key) values ({insertion_str})'
        cur.execute(insertion)
        conn.commit()
    cur.execute(f'select * from daily_reports;')
    if len(csv_file) != cur.rowcount:
        return fail(500, "insertions to the table are not finished appropriately",
                    "the number of rows in the table is different from the number of rows in the upcoming file")
    cur.close()
    conn.close()
    msg = jsonify({"message": "your file is successfully updated"})
    return make_response(msg, 200)


@daily_reports.route("/cases", methods=['POST'])
def query_data():
    data = request.get_json()

    required_parameters = ["return_type", "date", "types", "locations"]
    missing_required = check_request(required_parameters, data)
    if missing_required[0] != "" or missing_required[1] != "":
        return fail(400, "Missing required parameter(s)",
                    "Missing required parameter(s): " + missing_required[0] +
                    "\nMissing parameter \"Country/Region\" for location(s): " + missing_required[1])

    date = data["date"]
    types = data["types"]
    locations = data["locations"]

    if len(types) == 0:
        return fail(400, "Missing required parameter(s)", "Parameter \"types\" must be an non-empty array")
    if data["return_type"] != "json" and data["return_type"] != "csv":
        return fail(400, "Wrong parameter value", "Parameter \"return_type\" must be \"json\" or \"csv\"")

    try:
        conn = connect_database()
        cur = conn.cursor()

        cur.execute("SELECT last_update FROM daily_reports;")
        existed_daily_report = cur.fetchone()

        if existed_daily_report is None or \
                (datetime.strptime(existed_daily_report[0], '%Y-%m-%d %X') - timedelta(days=1)).strftime('%m/%d/%y') \
                != date:
            return fail(400, "No data for the given date", "No daily report existed for the given date")
        json_data = return_json(cur, date, locations, types)
        cur.close()
        conn.close()
        if data["return_type"] == "json":
            return_data = jsonify(json_data)
            content_type = "application/json"
        else:
            return_data = return_csv(json_data, types)
            content_type = "text/csv"
        response = make_response(return_data, 200, )
        response.headers["Content-Type"] = content_type
        return response
    except psycopg2.Error as e:
        return fail(400, "Postgresql Error", e.pgerror)
