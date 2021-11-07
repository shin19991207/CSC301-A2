# Query Time Series Data

Query data by countries, time period, and cases types to get the data of the COVID cases type specified.

**URL**: `/time_series/cases`

**Method**: `POST`

**Required Parameters:**

<table>
<tr> 
<td> Name </td> <td> Type </td> <td> Description </td> <td> Example </td>
</tr>
<tr>
<td> start_date </td>
<td> non-empty string </td>
<td> The starting date of the period in the format <code>"mm/dd/yy"</code>. <code>start_date</code> has to be a date that is one of the columns in the uploaded time series data </td>
<td> <code>"01/12/20"</code> </td>
</tr>
<tr>

<td> end_date </td>
<td> non-empty string </td>
<td> The ending date of the period in the format <code>mm/dd/yy</code>. <code>end_date</code> has to be a date that is one of the columns in the uploaded time series data and <code>start_date <= end_date</code> </td>
<td> <code>"01/22/20"</code> </td>
</tr>
<tr>

<td> types </td>
<td> non-emtpy array </td>
<td> An array with the following string as options:  <code>"Confirmed"</code>,  <code>"Deaths"</code>,  <code>"Recovered"</code>,  <code>"Active"</code> </td>
<td> <code>["Deaths", "Recovered"]</code> </td>
</tr>
<tr>

<td> locations </td>
<td> non-emtpy array of json object </td>
<td> Countries. Each json object in the array should contains the parameter <code>"Country/Region"</code>, which should be a value in the column Country/Region of the uploaded data; <code>"Province/State"</code> is an optional parameter, which should be a value in the column Province/State of the uploaded data if provided
</td>
<td> 

```json
[
 { "Country/Region": "Albania" }, 
 { "Country/Region": "Canada", 
   "Province/State": "Ontario" }, 
 { "Country/Region": "Australia" }
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
    "01/26/20": [
      {
        "Confirmed": 0, 
        "Country/Region": "Albania"
      }, 
      {
        "Confirmed": 1, 
        "Country/Region": "Canada", 
        "Province/State": "Ontario"
      }, 
      {
        "Confirmed": 0, 
        "Country/Region": "Australia"
      }
    ], 
    "01/27/20": [
      {
        "Confirmed": 0, 
        "Country/Region": "Albania"
      }, 
      {
        "Confirmed": 1, 
        "Country/Region": "Canada", 
        "Province/State": "Ontario"
      }, 
      {
        "Confirmed": 0, 
        "Country/Region": "Australia"
      }
    ], 
    "01/28/20": [
      {
        "Confirmed": 0, 
        "Country/Region": "Albania"
      }, 
      {
        "Confirmed": 1, 
        "Country/Region": "Canada", 
        "Province/State": "Ontario"
      }, 
      {
        "Confirmed": 0, 
        "Country/Region": "Australia"
      }
    ]
  }
  ```
  * Content-Type: `text/csv`
  * Returned data in csv format
  ```
  Date,Province/State,Country/Region,Confirmed
  01/26/20,,Albania,0
  01/26/20,Ontario,Canada,1
  01/26/20,,Australia,0
  01/27/20,,Albania,0
  01/27/20,Ontario,Canada,1
  01/27/20,,Australia,0
  01/28/20,,Albania,0
  01/28/20,Ontario,Canada,1
  01/28/20,,Australia,0     
  ```

**Error Response**

* **Code**: `400 Bad Request`
* **Content**: 
  ```json
  { 
    "code": 400, 
    "message": "Wrong parameter value", 
    "detail": "Parameter return_type must be json or csv" 
  }
  ```

OR

* **Code**: `500 Internal Server Error`
* **Content**: 
  ```json
  { 
    "code": 500, 
    "message": "Internal Server Error", 
    "detail": "PlpgsqlError" 
  }
  ```

**Sample Call**:
```
$ curl -d '{ "return_type" : "json",
             "start_date": "02/21/20",
             "end_date": "2/26/20",
             "types": ["Confirmed"],
             "locations":
                [ {"Country/Region": "Albania"},  
                  {"Country/Region": "Canada", "Province/State": "Ontario"},
                  {"Country/Region": "Australia"}
                ]
           }' 
        -H "Content-Type: application/json" 
        -X POST https://covid-monitor-61.herokuapp.com/time_series/cases
```

