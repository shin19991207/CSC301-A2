### API description

Upload or update a daily reports formatted csv file data.



**The format of the file to upload/update:** the format follows the "daily_reoports" file specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)



**The way to make request with csv file**:

 (Step 1) Download the desired csv file from the repo [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) if not already or you can use any csv file in the same format

 (Step 2) Navigate to the folder containing the csv file in your terminal

 (Step 3) Pass request body by specifying the relative path of the file to the folder running the request command. ie:`@[file name]`

For example, if you download the csv file to the **Desktop folder** in your computer, then you only need to pass `@01-01-2021.csv` as a request body when running the request commend in the terminal navigated to the **Desktop folder**

**URL**: `/daily_reports/data`

**Method**: `POST`

**Request Body**:

| Name | Type     | Required | Description                       | Example             |
| ---- | -------- | -------- | --------------------------------- | ------------------- |
| data | text/csv | Yes      | The relative path of the csv file | `"@01-01-2021.csv"` |



**Success Response**:

* **Code**: `200 OK`
* **Content**: `{"message": "your file is successfully updated"}`


**Error Response**:

* **Code**: `400 Bad Request`
* **Content**: 

```json
{
 "code": 400,
 "detail": "numbers of people should be integers",
 "message": "the content of the upcoming file does not meet expectation"
}
```



**Sample Call**:

```
$ curl -H "Content-Type: text/csv" \
  --data-binary "@01-01-2021.csv" \
  -X POST https://covid-monitor-61.herokuapp.com/daily_reports/data
```