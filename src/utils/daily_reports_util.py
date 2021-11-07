import psycopg2
import copy


def return_json(cur, date, locations, types):
    return_data = {"Date": date, "Reports": []}
    for location in locations:
        location_data = copy.deepcopy(location)
        if "Combined_Key" in location:
            query = "SELECT sum(confirmed), sum(deaths), sum(recovered), sum(active)" \
                    "FROM daily_reports WHERE combined_key = {0} GROUP BY combined_key;" \
                .format(location['Country/Region'])
        elif "Province/State" not in location:
            query = "SELECT sum(confirmed), sum(deaths), sum(recovered), sum(active)" \
                    "FROM daily_reports WHERE region = {0} GROUP BY region;" \
                .format(location['Country/Region'])
        else:
            query = "SELECT sum(confirmed), sum(deaths), sum(recovered), sum(active)" \
                    "FROM daily_reports WHERE region = {0} and state = {1} GROUP BY region, state;" \
                .format(location['Country/Region'], location['Province/State'])
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


def return_csv(json_data, types):
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
