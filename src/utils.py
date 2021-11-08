import psycopg2
import copy
from flask import jsonify, make_response


def daily_reports_return_json(cur, date, locations, types, table_name):
    return_data = {"Date": date, "Reports": []}
    for location in locations:
        location_data = copy.deepcopy(location)

        location['Country/Region'] = location['Country/Region'].replace("'", "''")
        if 'Province/State' in location:
            location['Province/State'] = location['Province/State'].replace("'", "''")
        if 'Combined_Key' in location:
            location['Combined_Key'] = location['Combined_Key'].replace("'", "''")

        if "Combined_Key" in location:
            query = "SELECT sum(confirmed), sum(deaths), sum(recovered), sum(active)" \
                    "FROM {0} WHERE combined_key = '{1}' GROUP BY combined_key;" \
                .format(table_name, location['Combined_Key'])
        elif "Province/State" not in location:
            query = "SELECT sum(confirmed), sum(deaths), sum(recovered), sum(active)" \
                    "FROM {0} WHERE region = '{1}' GROUP BY region;" \
                .format(table_name, location['Country/Region'])
        else:
            query = "SELECT sum(confirmed), sum(deaths), sum(recovered), sum(active)" \
                    "FROM {0} WHERE region = '{1}' and state = '{2}' GROUP BY region, state;" \
                .format(table_name, location['Country/Region'], location['Province/State'])
        cur.execute(query)
        record = cur.fetchone()
        for type in types:
            if type == "Confirmed":
                location_data[type] = None if record is None else record[0]
            elif type == "Deaths":
                location_data[type] = None if record is None else record[1]
            elif type == "Recovered":
                location_data[type] = None if record is None else record[2]
            else:
                location_data[type] = None if record is None else record[3]
        return_data['Reports'].append(location_data)
    return return_data


def daily_reports_return_csv(json_data, types):
    return_data = "Date,Province/State,Country/Region,Combined_Key"
    for type in types:
        return_data += ("," + type.capitalize())
    for row in json_data['Reports']:
        province_state = "" if 'Province/State' not in row else row['Province/State']
        combined_key = "" if 'Combined_Key' not in row else row['Combined_Key']
        row_str = "\n{0},{1},{2},{3}".format(json_data['Date'], province_state, row['Country/Region'], combined_key)
        for type in types:
            count = "" if row[type] is None else row[type]
            row_str += ("," + str(count))
        return_data += row_str
    return return_data


def time_series_return_csv(json_data, date_range, types):
    return_data = "Date,Province/State,Country/Region"
    for type in types:
        return_data += ("," + type)
    for date in date_range:
        for row in json_data[date]:
            province_state = "" if 'Province/State' not in row else row['Province/State']
            row_str = "\n{0},{1},{2}".format(date, province_state, row['Country/Region'])
            for type in types:
                count = "" if row[type] is None else row[type]
                row_str += ("," + str(count))
            return_data += row_str
    return return_data


# check if the current data base contains all data (confirmed, recovered, deaths) needed to calculate active
def check_query_data_active(cur, needed_types):
    for needed_type in needed_types:
        try:
            cur.execute("SELECT * FROM {0};".format(needed_type))
        except psycopg2.Error:
            return False
    return True


# return error message to help users to change request
def fail(code, message, detail):
    return_data = jsonify({'code': code, 'message': message, 'detail': detail})
    response = make_response(return_data, code, )
    return response


def check_request(required_parameters, json_data):
    missing_parameters = []
    missing_parameters_str = ""
    missing_country_region_str = ""
    for parameter in required_parameters:
        if parameter not in json_data:
            missing_parameters.append(parameter)
    missing_country_region = []
    if 'locations' in json_data:
        for location in json_data['locations']:
            if 'Country/Region' not in location:
                missing_country_region.append(location)

    if len(missing_parameters) != 0:
        for parameter in missing_parameters[: -1]:
            missing_parameters_str += (parameter + ", ")
        missing_parameters_str += (missing_parameters[-1])
    if len(missing_country_region) != 0:
        for location in missing_country_region[: -1]:
            missing_country_region_str += (location + ", ")
        missing_country_region_str += (missing_country_region[-1])
    return [missing_parameters_str, missing_country_region_str]
