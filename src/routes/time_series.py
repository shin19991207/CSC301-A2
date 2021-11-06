from flask import Blueprint, request, jsonify
# import csv
# import codecs
import psycopg2
from io import StringIO
from datetime import datetime
import pandas as pd
from utils.time_series_util import return_json, check_request
from config import connect_database

time_series = Blueprint('time_series', __name__)

format = ['Province/State', 'Country/Region', 'Lat', 'Long']


# Test: curl -H "Content-Type: multipart/form-data" -F "file=@mydata.csv" http://localhost:5000/myroute
# curl -H "Content-Type: text/csv" --data-binary "@datafile.csv" http://localhost:5000/myroute
@time_series.route("/data", methods=['POST'])
def load_data():
    if not request.content_type.startswith('text/csv'):
        return "error: content type"
    if request.headers.get('type') is None:
        return "error: type not specified. type can be confirmed, active, deaths, recovered."
    elif request.headers.get('type') not in ['confirmed', 'deaths', 'recovered', 'active']:
        return "type should be one of confirmed, active, deaths, recovered."

    table_name = request.headers.get('type')

    data_content = request.data.decode('utf-8')
    buffer = StringIO()
    buffer.write(data_content)
    buffer.seek(0)
    table_columns = buffer.readline()

    if table_columns.strip().split(',')[0:4] != format:
        return "error: format"

    # list of formatted dates, each date is a column in the table
    formatted_dates = []
    for date in table_columns.strip().split(',')[4:]:
        # format date into format mm/dd/yy
        formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%m/%d/%y')
        formatted_dates.append(formatted_date)
    print(formatted_dates)

    buffer.seek(0)
    input_csv = pd.read_csv(buffer, sep=",", header=0, index_col=False)
    input_json = input_csv.to_dict(orient='list')
    print(input_json['Country/Region'])

    # line = buffer.readline()
    # data = []
    # while line:
    #     row = line.strip().split(',')
    #     row.pop(2)
    #     row.pop(3)
    #     data.append(row)
    #     line = buffer.readline()
    # print(data[0])

    # conn = connect_database()
    # cur = conn.cursor()
    # # cur.execute("insert into testtable values (2);")
    # cur.close()
    # conn.commit()
    # conn.close()

    return "success"


@time_series.route("/cases", methods=['POST'])
def query_data():
    data = request.get_json()
    missing_required = check_request(data)
    if missing_required[0] != "" or missing_required[1] != "":
        return "Missing required parameter(s): " + missing_required[0] + \
               "\nMissing parameter \"Country/Region\" for location(s): " + missing_required[1]

    if len(data["types"]) == 0:
        return "Parameter \"types\" must be an non-empty array"

    start_date = data["start_date"]
    end_date = data["end_date"]
    types = data["types"]
    locations = data["locations"]

    # get date range as list of dates
    date_range = []
    dates = pd.date_range(start=datetime.strptime(start_date, '%m/%d/%y'),
                          end=datetime.strptime(end_date, '%m/%d/%y')).to_pydatetime().tolist()
    for date in dates:
        date_range.append(date.strftime('%m/%d/%y'))

    try:
        conn = connect_database()
        cur = conn.cursor()
        if data["return_type"] == "json":
            json_data = return_json(cur, date_range, locations, types)
            return jsonify(json_data)
        else:
            return "csv file"
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(e.pgerror)
        print(e.diag.message_detail)
        return "error"

    return "success"

# def return_csv():
#

