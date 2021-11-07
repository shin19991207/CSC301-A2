import psycopg2
import copy


def return_json(cur, date_range, locations, types):
    return_data = {}
    for date in date_range:
        return_data[date] = []
        for location in locations:
            location_data = copy.deepcopy(location)
            location['Country/Region'] = location['Country/Region'].replace("'", "''")
            if 'Province/State' in location:
                location['Province/State'] = location['Province/State'].replace("'", "''")
            for type in types:
                records = {}                
                location_str = "region = '{0}'".format(location['Country/Region']) \
                    if "Province/State" not in location \
                    else "region = '{0}' AND state = '{1}'".format(location['Country/Region'], location['Province/State'])
                if type == "Confirmed" or type == "Active":
                    confirmed_query = "SELECT sum(\"{0}\") FROM Confirmed WHERE ".format(date) + \
                                      location_str + " GROUP BY region, state;"
                    cur.execute(confirmed_query)
                    confirmed_record = cur.fetchone()
                    records['Confirmed'] = None if confirmed_record is None else confirmed_record[0]
                if type == "Deaths" or type == "Active":
                    deaths_query = "SELECT sum(\"{0}\") FROM Deaths WHERE ".format(date) + \
                                      location_str + " GROUP BY region, state;"
                    cur.execute(deaths_query)
                    deaths_record = cur.fetchone()
                    records['Deaths'] = None if deaths_record is None else deaths_record[0]
                if type == "Recovered" or type == "Active":
                    recovered_query = "SELECT sum(\"{0}\") FROM Deaths WHERE ".format(date) + \
                                      location_str + " GROUP BY region, state;"
                    cur.execute(recovered_query)
                    recovered_record = cur.fetchone()
                    records['Recovered'] = None if recovered_record is None else recovered_record[0]
                location_data[type] = records[type.capitalize()] if type.capitalize() != "Active" \
                    else records['Confirmed'] - records['Deaths'] - records['Recovered']
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


