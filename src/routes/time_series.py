from flask import Blueprint, request
import csv
import codecs

time_series = Blueprint('time_series', __name__)


# Test: curl -H "Content-Type: multipart/form-data" -F "file=@mydata.csv" http://localhost:5000/myroute
@time_series.route("/data", methods=['POST'])
def load_data():
    file = request.files['file']
    # print(data['file'].read())
    data = []
    stream = codecs.iterdecode(file.stream, 'utf-8')
    for row in csv.reader(stream, dialect=csv.excel):
        if row:
            data.append(row)
    print(data[0])

    file_name = file.filename
    print(file_name)

    return "success"


@time_series.route("/cases", methods=['POST'])
def query_data():
    return
