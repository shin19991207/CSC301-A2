from flask import Blueprint, request, jsonify, make_response
import psycopg2
from io import StringIO
from datetime import datetime
import pandas as pd
from config import connect_database
from utils.time_series_util import return_json, return_csv, check_query_data_active
from utils.util import fail, check_request

time_series = Blueprint('time_series', __name__)
# TODO: use regular expression to make sure that there is at least one date
hard_column = ["Province/State", "Country/Region", "Lat", "Long"]


# Test: curl -H "Content-Type: multipart/form-data" -F "file=@mydata.csv" http://localhost:5000/myroute
# curl -H "Content-Type: text/csv" --data-binary "@datafile.csv" http://localhost:5000/myroute
@time_series.route("/data", methods=['POST'])
def load_data():
    # check the format and type parameter
    if not request.content_type.startswith('text/csv'):
        return fail(400, "content type is not correct", "please check if your file is a csv file")
    if request.headers.get('type') not in ['confirmed', 'deaths', 'recovered', 'active']:
        return fail(400, "content type is not correct", "type argument should be one of confirmed, active, "
                                                        "deaths, recovered.")

    # read in binary data (csv file)
    table_name = request.headers.get('type')
    data_content = request.data.decode('utf-8')
    buffer = StringIO()
    buffer.write(data_content)
    buffer.seek(0)
    zero_row = buffer.readline().strip().split(',')
    buffer.seek(0)
    csv_file = pd.read_csv(buffer)
    Lat = csv_file['Lat']
    Long = csv_file['Long']
    # check the data type
    if Lat.dtypes == "object" or Long.dtypes == "object":
        return fail(400, "datatype error in Lat and Long column", "Latitude and Longitude should be floats or "
                                                                  "integers and nothing else")

    # check the range of latitude and longitude
    if Lat.max() > 90 or Lat.min() < -90 or Long.max() > 180 or Long.max() < -180:
        return fail(400, "error occur in Lat and Long column in the file ", "Latitudes range from -90 to 90 "
                                                                            "inclusively, and longitudes range from "
                                                                            "-180 to 80 "
                                                                            " inclusively")

    # check if the column of upcoming file are the same as files in github repo
    if zero_row[0:4] != hard_column:
        return fail(400, "the content of the upcoming file does not meet expectation",
                    "please check if your file miss a column suggested in the "
                    "link:https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data"
                    "/csse_covid_19_time_series")

    # TODO: check whether the value of country and region are strings

    # check if the numbers of people in the column are integers
    types = csv_file.iloc[:, 4:].dtypes
    for index, value in types.items():
        if value != "int64":
            return fail(400, "the content of the upcoming file does not meet expectation",
                        "numbers of people should be integers")

    conn = connect_database()
    cur = conn.cursor()
    cur.execute(f'drop table if exists {table_name}')
    conn.commit()
    fixed = f'create table {table_name} (State VARCHAR ( 100 ), Region VARCHAR ( 100 )'
    dates_create = ""
    column_name = "State,Region"
    acc_column = 2
    for date in zero_row[4:]:
        acc_column += 1
        # format date into format mm/dd/yy
        formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%m/%d/%y')
        dates_create = dates_create + f',"{formatted_date}" integer'
        column_name = f'{column_name},"{formatted_date}"'
    # create table
    cur.execute(f'{fixed + dates_create})')
    conn.commit()
    for i in range(len(csv_file)):
        state = str(csv_file.iloc[i, 0])
        modified_state = state.replace("'", "''")
        region = str(csv_file.iloc[i, 1])
        modified_region = region.replace("'", "''")
        insertion_str = f"'{modified_state}', '{modified_region}'"
        print("insert str", insertion_str)
        acc_value = 2

        for j in range(4, len(csv_file.iloc[i, :])):
            acc_value += 1
            insertion_str = insertion_str + ',' + str(csv_file.iloc[i, j])
        insertion = f'insert into {table_name}({column_name}) values ({insertion_str})'
        print("insertion str\n", insertion_str)
        cur.execute(insertion)
        conn.commit()

    cur.close()
    conn.commit()
    conn.close()
    return "success"


@time_series.route("/cases", methods=['POST'])
def query_data():
    data = request.get_json()

    required_parameters = ['return_type', 'start_date', 'end_date', 'types', 'locations']
    missing_required = check_request(required_parameters, data)
    if missing_required[0] != "" or missing_required[1] != "":
        return fail(400, "Missing required parameter(s)",
                    "Missing required parameter(s): " + missing_required[0] +
                    "\nMissing parameter \"Country/Region\" for location(s): " + missing_required[1])

    start_date = data["start_date"]
    end_date = data["end_date"]
    types = data["types"]
    locations = data["locations"]

    if len(types) == 0:
        return fail(400, "Missing required parameter(s)", "Parameter types must be an non-empty array")
    print(data["return_type"])

    if data["return_type"] != "json" and data["return_type"] != "csv":
        return fail(400, "Wrong parameter value", "Parameter return_type must be json or csv")

    # get date range as list of dates
    date_range = []
    dates = pd.date_range(start=datetime.strptime(start_date, '%m/%d/%y'),
                          end=datetime.strptime(end_date, '%m/%d/%y')).to_pydatetime().tolist()
    for date in dates:
        date_range.append(date.strftime('%m/%d/%y'))

    try:
        conn = connect_database()
        cur = conn.cursor()
        if "Active" in types and not check_query_data_active(cur):
            return fail(400, "Missing required data", "Not enough data in the database to calculate type Active")
        json_data = return_json(cur, date_range, locations, types)
        cur.close()
        conn.close()
        if data["return_type"] == "json":
            return_data = jsonify(json_data)
            content_type = "application/json"
        else:
            return_data = return_csv(json_data, date_range, types)
            content_type = "text/csv"
        response = make_response(return_data, 200, )
        response.headers["Content-Type"] = content_type
        return response
    except psycopg2.Error as e:
        print(e.diag.message_detail)
        return fail(500, "Internal Server Error", e.pgerror)
