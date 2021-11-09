**URL**: `/time_series/data?type={type}`

**Method**: `POST`

**Required Body**:

| Name | Type     | Description                                                  | Example                                       |
| ---- | -------- | ------------------------------------------------------------ | --------------------------------------------- |
| data | text/csv | 1. The format of the file: the format follows the "times series" file specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series). <br/><br/> **IMPORTANT NOTICE**: we only accept the file in the format of global time_series such as [files with titles end with global in the repo](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv) instead of [files with titles end with US](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv)<br/><br/> 2. The way to make request with csv file<br/> (Step 1) Download the desired csv file from the repo [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) if not already<br/> (Step 2) Navigate to the folder containing the csv file in your terminal<br/> (Step 3) Pass request body by the relative path of the file to the place running the request command. ie:`@[file name]`    <br/><br/>For example, if you download the file to the **Desktop folder** in your computer, then you only need to pass `@time_series_covid19_confirmed_global.csv` as a request body when running the request commend in the terminal navigated to the **Desktop folder** | `"@time_series_covid19_confirmed_global.csv"` |

**Required Param**:

| Name | Type    | Description                                                  | Example     |
| ---- | ------- | ------------------------------------------------------------ | ----------- |
| type | param | The cases type of the provided time series file. It should be one of: `confirmed`, `deaths`, `recovered` or  `active`. Notice that the type is specified in the title of the file. <br/><br/>**For example**, if you upload file `time_series_covid19_confirmed_global.csv`, then you need to pass parameter type as `confirmed` | `confirmed` |

**Success Response**:

* **Code**: `200 OK`
* **Content**: 
    ```json
    {"message": "your file 'daily_reports' is successfully loaded/updated"}
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
  --data-binary "@time_series_covid19_confirmed_global.csv" \
  -X POST https://covid-monitor-61.herokuapp.com/time_series/data?type=confirmed
```

