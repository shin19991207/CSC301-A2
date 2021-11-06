from flask import Blueprint, request, jsonify
import csv
import codecs
import psycopg2
from io import StringIO
from datetime import datetime
from routes.config import connect_database


time_series = Blueprint('time_series', __name__)
# TODO: use regular expression to make sure that there is at least one date
hard_column = ["Province/State", "Country/Region", "Lat", "Long"]


# Test: curl -H "Content-Type: multipart/form-data" -F "file=@mydata.csv" http://localhost:5000/myroute
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
    print("result", ",".join(first_row[:2] + first_row[4:]))
    # insertion = f'insert into {table_name}({",".join(first_row[:2] + first_row[4:])}) values ({values})'
    # cur.close()
    # conn.commit()
    # conn.close()

    return "success"


@time_series.route("/cases", methods=['POST'])
def query_data():
    return


if __name__ == '__main__':
    print("success")
