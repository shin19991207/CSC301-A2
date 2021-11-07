import psycopg2
import copy


def return_json(cur, date_range, locations, types):
    return_data = {}
    for date in date_range:
        return_data[date] = []
        for location in locations:
            location_data = copy.deepcopy(location)
            for type in types:
                if "Province/State" not in location:
                    query = "SELECT sum({0})" \
                            "FROM {1} WHERE region = {2} " \
                            "GROUP BY region;" \
                        .format(date, type, location['Country/Region'])
                else:
                    query = "SELECT sum({0})" \
                            "FROM {1} " \
                            "WHERE region = {2} AND state = {3}" \
                            "GROUP BY region, state;" \
                        .format(date, type, location['Country/Region'], location['Province/State'])
                cur.execute(query)
                record = cur.fetchone()
                location_data[type] = None if record is None else record[0]
            return_data[date].append(location_data)
    return return_data


def return_csv(json_data, date_range, types):
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
def check_query_data_active(cur):
    needed_types = ["Confirmed", "Deaths", "Recovered"]
    for type in needed_types:
        query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = {0});".format(type)
        cur.execute(query)
        if cur.fetchone()[0] == 'f':
            return False
    return True


