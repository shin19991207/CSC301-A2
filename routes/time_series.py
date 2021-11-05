from flask import Blueprint, request

time_series = Blueprint('time_series', __name__)

@time_series.route("/data", methods=['POST'])
def load_data():
    data = request.get_data()
    print(data)
    return "success"

@time_series.route("/cases", methods=['POST'])
def query_data():
    return