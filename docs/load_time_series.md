# Load Time Series Data

Upload or update a time series formatted csv file data.

## Add data / Update data

**URL**: `/time_series/data`

**Method**: `POST`

**Required Body**:

| Name | Type     | Description                                                  | Example                                       |
| ---- | -------- | ------------------------------------------------------------ | --------------------------------------------- |
| data | text/csv | The cvs file in the form of global time series files following the format specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) | `"@time_series_covid19_confirmed_global.csv"` |

**Required Headers**:

| Name | Type    | Description                                                  | Example     |
| ---- | ------- | ------------------------------------------------------------ | ----------- |
| type | headers | The cases type of the provided time series file. It should be one of: `confirmed`, `deaths`, `recovered` or  `active` | `confirmed` |

**Success Response**:

* **Code**: `200 OK`
* **Content**: 
    ```json
    {"message": "your file 'daily_reports' is successfully updated"}
    ```
  


**Error Response**:

* **Code**: `400 Bad Request`

* **Content**: 

  ```json
  {
  "code": 400,
  "detail": "please check if your file is a csv file",
  "message": "content type is not correct"
  }
  ```

- **Code**: `500 Internal Server Error `

- **Content**: 

  ```json
  {
  "code": 500,
  "detail": "please check if your file is a csv file",
  "message": "content type is not correct"
  }
  ```

  


**Sample Call**:

```
$ curl -H "Content-Type: text/csv" \
  -H "type: Confirmed" \
  --data-binary "@time_series_covid19_confirmed_global.csv" \
  -X POST https://covid-monitor-61.herokuapp.com/time_series/data
```