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

format = ['Province/State', 'Country/Region', 'Lat', 'Long']


# Test: curl -H "Content-Type: multipart/form-data" -F "file=@mydata.csv" http://localhost:5000/myroute
# curl -H "Content-Type: text/csv" --data-binary "@datafile.csv" http://localhost:5000/myroute
@time_series.route("/data", methods=['POST'])
def load_data():
    # check the format and type parameter
    if not request.content_type.startswith('text/csv'):
        return jsonify({'code': 400,
                        'message': "content type is not correct",
                        'detail': "please check if your file is a csv file"})
    if request.headers.get('type') is None or request.headers.get('type') not in ['confirmed', 'deaths',
                                                                                  'recovered', 'active']:
        return jsonify({'code': 400,
                        'message': "content type is not correct",
                        'detail': "type argument should be one of confirmed, active, deaths, recovered."})

    # read in binary data (csv file)
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
    input_csv = pd.DataFrame(pd.read_csv(buffer, sep=",", header=0, index_col=False))
    # print(input_csv)
    data = []
    for index, row in input_csv.iterrows():
        row_data = []
        for key in row:
            row_data.append(key)
        data.append(row_data)
    print(data[0])
    # input_json = input_csv.to_dict(orient='index')
    # print(input_json)

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
    first_row = table_columns.strip().split(',')

    # prepare create table statement
    if first_row[0:4] != hard_column:
        return jsonify({'code': 400,
                        'message': "the content of the upcoming file does not meet expectation",
                        'detail': "please check if your file miss a column suggested in the link below",
                        'help': "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series"})
    conn = connect_database()
    cur = conn.cursor()
    fixed = f'create table "{table_name}" (State VARCHAR ( 100 ), ' \
            f'Region VARCHAR ( 100 ), ' \
            f'Lat float(50), ' \
            f'Long float(50)'
    dates_type = ""
    for date in first_row[4:]:
        # format date into format mm/dd/yy
        formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%m/%d/%y')
        dates_type = dates_type + f',"{formatted_date}" integer'

    # create table
    # cur.execute(f'{fixed + dates_type})')

    # prepare insert rows statement
    line = buffer.readline()
    msg = {'code': 400,
           'message': "error occur in Lat and Long column in the file ",
           'detail': "Latitudes range from -90 to 90 inclusively, and longitudes range from -180 to 80"
                     " inclusively"}
    while line:
        row = line.strip().split(',')
        lat = row[2]
        long = row[3]
        print("lat", row[2])
        if row[2] and (float(row[2]) > 90.0 or float(row[2]) < -90.0):
            return jsonify(msg)
        if row[3] and (float(row[3]) > 180.0 or float(row[3]) < -180.0):
            return jsonify(msg)
        line = buffer.readline()
        row.pop(2)
        row.pop(3)
    # print("result", ",".join(first_row[:2] + first_row[4:]))
    # insertion = f'insert into {table_name}({",".join(first_row[:2] + first_row[4:])}) values ({values})'
    # cur.close()
    # conn.commit()
    # conn.close()

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
        return fail(400, "Missing required parameter(s)", "Parameter \"types\" must be an non-empty array")

    if data["return_type"] != "json" or data["return_type"] != "csv":
        return fail(400, "Wrong parameter value", "Parameter \"return_type\" must be \"json\" or \"csv\"")

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
        response = make_response(jsonify({"Data": return_data}), 200, )
        response.headers["Content-Type"] = content_type
        return response
    except psycopg2.Error as e:
        return fail(502, e.pgerror, e.diag.message_detail)



