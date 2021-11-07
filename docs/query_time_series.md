# Time Series Query Data

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

  * json format returned data

    ```json
    { 
    }
    ```

  * [x] for csv data
    
    ```
    
    ```

**Error Response**

Code: `400 Bad Request`

Code: `500 Internal Server Error`

