### API description

Query data by countries, time period, and cases types to get the data of the COVID cases type specified.

**IMPORTANT NOTICE**:

Due to the limitation of database storage, we will not storing the file uploaded before and thus, if you want to query on a csv file, you need to upload it first.

**URL**: `/daily_reports/cases`

**Method**: `POST`

**Content-Type**: `application/json`

**Required Body:**

<table>
<tr> 
<td> Name </td> <td> Type </td> <td> Description </td> <td> Example </td>
</tr>

<td> types </td>
<td> non-emtpy array </td>
<td> An array with the following string as options:  <code>"Confirmed"</code>,  <code>"Deaths"</code>,  <code>"Recovered"</code>,  <code>"Active"</code> </td>
<td> <code>["Deaths", "Recovered"]</code> </td>
</tr>
<tr>

<td> locations </td>
<td> non-emtpy array of json object </td>
<td> Countries. Each json object in the array should contains the parameter <code>"Country/Region"</code>, which should be a value in the column Country/Region of the uploaded data; <code>"Province/State"</code> and <code>"Combined_Key"</code> are optional parameters and should be a value in the column Province/State and Combined_Key of the uploaded data respectively, if provided
</td>
<td> 

```json
[
  { 
    "Country/Region": "Belgium"
  },
  { 
    "Country/Region": "Canada", 
    "Province/State": "Ontario"
  },
  { 
    "Country/Region": "Australia", 
    "Province/State": "Australian Capital Territory",
    "Combined_Key": "Australian Capital Territory, Australia"
  }
]
```
</td>
</tr>
<tr>

<td> return_type </td>
<td> non-empty string </td>
<td> Format of the returned data; Should be one of <code>"json"</code> or <code>"csv"</code>
</td>
<td> 
<code>"json"</code>
</td>
</tr>
</table>

**Success Response**

* Code: `200`
* Content:
  * Content-Type: `application/json`
  * Returned data in json format
  ```json
  {
      "Date": "01/01/21",
      "Reports": [
          {
              "Active": 628708,
              "Confirmed": 648289,
              "Country/Region": "Belgium",
              "Deaths": 19581
          },
          {
              "Active": 20154,
              "Confirmed": 187344,
              "Country/Region": "Canada",
              "Deaths": 4568,
              "Province/State": "Ontario"
          },
          {
              "Active": 1,
              "Combined_Key": "Australian Capital Territory, Australia",
              "Confirmed": 118,
              "Country/Region": "Australia",
              "Deaths": 3,
              "Province/State": "Australian Capital Territory"
          }
      ]
  }
  ```
  
  * Content-Type: `text/csv`
  * Returned data in csv format
  ```
  Date,Province/State,Country/Region,Combined_Key,Confirmed,Deaths,Active
  01/01/21,,Belgium,,648289,19581,628708
  01/01/21,Ontario,Canada,,187344,4568,20154
  01/01/21,Australian Capital Territory,Australia,Australian Capital Territory, Australia,118,3,1
  ```

**Error Response**

* **Code**: `400 Bad Request`
* **Content**: 
  ```json
  { 
    "code": 400, 
    "message": "No data for the given date", 
    "detail": "No daily report existed for the given date" 
  }
  ```


**Sample Call**:
```
$ curl --location --request POST 'https://covid-monitor-61.herokuapp.com/daily_reports/cases' \
  --header 'Content-Type: application/json' \
  --data-raw '{ "return_type" : "json",  
                "types": [ "Confirmed", "Deaths", "Active" ],
                "locations":
                [
                  { "Country/Region": "Belgium" },
                  { "Country/Region": "Canada", 
                    "Province/State": "Ontario" },
                  { "Country/Region": "Australia", 
                    "Province/State": "Queensland", 
                    "Combined_Key": "Australian Capital Territory, Australia" }
                ]
              }'
```

