from flask import jsonify, make_response


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


