import copy


def check_request(json_data):
    required_parameters = ['return_type', 'start_date', 'end_date', 'types', 'locations']
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


def return_json(cur, date_range, locations, types):
    return_data = {}
    for date in date_range:
        return_data[date] = []
        for location in locations:
            location_data = copy.deepcopy(location)
            for type in types:
                if "Province/State" not in location:
                    query = "SELECT sum({0})" \
                            "FROM {1} WHERE Location = {2} " \
                            "GROUP BY \"Country/Region\";" \
                        .format(date, type, location['Country/Region'])
                else:
                    query = "SELECT sum({0})" \
                            "FROM {1} " \
                            "WHERE \"Country/Region\" = {2} AND \"Province/State\" = {3}" \
                            "GROUP BY \"Country/Region\", \"Province/State\";" \
                        .format(date, type, location['Country/Region'], location['Province/State'])
                cur.execute(query)
                record = cur.fetchone()
                location_data[type] = None if record is None else record[0]
            return_data[date].append(location_data)
    return return_data
