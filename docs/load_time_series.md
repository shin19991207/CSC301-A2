# Time Series Load Data
Upload or update a time series formatted file.

## Add data / Update data

**URL**: `/time_series/data`

**Method**: `POST`

**Required Body**:

| Name | Type   | Description                                                  | Example                                                      |
| -----| ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| data | text/csv | The cvs file in the form of global time series files specified in the github https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series | `"@time_series_covid19_confirmed_global.csv"` |

**Required Headers**:

| Name      | Type   | Description                                                  | Example                                                      |
| --------- |------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| type | string | The cases type of the provided time series file. It should be one of: `Confirmed`, `Deaths`, `Recovered`, or `Active` | `"Confirmed"`                     |

**Success Response**:

* **Code**: `200 OK`
* **Content**: `{}`


**Error Response**:

* **Code**: `400 Bad Request`
* **Content**: `{}`

**Sample Call**:
```
$ curl -H "Content-Type: text/csv" \
  --data-binary "@time_series_covid19_confirmed_global.csv" \
  -X POST https://covid-monitor-61.herokuapp.com/time_series/data
```