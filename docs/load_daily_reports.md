# Load Daily Reports Data
Upload or update a daily reports formatted csv file data.

## Add data / Update data

**URL**: `/daily_reports/data`

**Method**: `POST`

**Required Body**:

| Name | Type   | Description                                                  | Example                                                      |
| -----| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| data | text/csv | The cvs file in the form of global daily reports files following the format specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) | `"@01-01-2021.csv"` |

**Success Response**:

* **Code**: `200 OK`
* **Content**: `{}`


**Error Response**:

* **Code**: `400 Bad Request`
* **Content**: `{}`

OR

* **Code**: `500 Internal Server Error`
* **Content**: `{}`

**Sample Call**:
```
$ curl -H "Content-Type: text/csv" \
  --data-binary "@01-01-2021.csv" \
  -X POST https://covid-monitor-61.herokuapp.com/daily_reports/data
```