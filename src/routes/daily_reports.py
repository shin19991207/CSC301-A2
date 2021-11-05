from flask import Blueprint

daily_reports = Blueprint('daily_reports', __name__)

@daily_reports.route("/data", methods=['POST'])
def load_data():
    return

@daily_reports.route("/cases", methods=['POST'])
def query_data():
    return