from flask import Blueprint, request, jsonify, make_response
import psycopg2
from io import StringIO
from datetime import datetime
import pandas as pd
from config import connect_database
from utils.daily_reports_util import return_json, return_csv
from utils.util import fail, check_request

daily_reports = Blueprint('daily_reports', __name__)


@daily_reports.route("/data", methods=['POST'])
def load_data():
    return


@daily_reports.route("/cases", methods=['POST'])
def query_data():
    data = request.get_json()

    required_parameters = ["return_type", "date", "types", "locations"]
    missing_required = check_request(required_parameters, data)
    if missing_required[0] != "" or missing_required[1] != "":
        return fail(400, "Missing required parameter(s)",
                    "Missing required parameter(s): " + missing_required[0] +
                    "\nMissing parameter \"Country/Region\" for location(s): " + missing_required[1])
    
    date = data["start_date"]
    types = data["types"]
    locations = data["locations"]
    
    if len(types) == 0:
        return fail(400, "Missing required parameter(s)", "Parameter \"types\" must be an non-empty array")
    if data["return_type"] != "json" or data["return_type"] != "csv":
        return fail(400, "Wrong parameter value", "Parameter \"return_type\" must be \"json\" or \"csv\"")

    try:
        conn = connect_database()
        cur = conn.cursor()
        
        cur.execute("SELECT date FROM daily_report_date;")
        existed_daily_report = cur.fetchone()
        if existed_daily_report is None or \
                existed_daily_report[0] != datetime.strptime(date, '%m/%d/%y').strftime('%m/%d/%y'):
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
        response = make_response(jsonify({"Data": return_data}), 200, )
        response.headers["Content-Type"] = content_type
        return response
    except psycopg2.Error as e:
        return fail(502, e.pgerror, e.diag.message_detail)