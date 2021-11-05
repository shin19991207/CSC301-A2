from flask import Blueprint

time_series = Blueprint('time_series', __name__)

@time_series.route("/data", methods=['POST'])
def load_data():
    return

@time_series.route("/cases", methods=['POST'])
def query_data():
    return