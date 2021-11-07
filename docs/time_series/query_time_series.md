#### Query data

**URL**: /time_series/cases

**Method**: POST

**Required Parameters:**

| Name         | Type             | Description                                                  | Example                   |
| ------------ | ---------------- | ------------------------------------------------------------ | ------------------------- |
| countries    | non-emtpy  array | Countries                                                    | `["US", "Canada"]`        |
| patient_type | non-emtpy array  | an array of the following string: "deaths", "confirmed", "recovered" | `["deaths", "recovered"]` |
| data_type    | non-emtpy string | type of the patient data returned. The data can be returned in cvs or JSON | `"JSON"`                  |

**Optional Parameters**:

| Name           | Type            | Description                     | Example      |
| -------------- | --------------- | ------------------------------- | ------------ |
| start_time     | non-null string | the time in the format mm/dd/yy | `"01/12/20"` |
| end_time       | nullable string |                                 | `"01/17/20"` |
| province_state | string          |                                 | `"Alabama"`  |

**Success Response**

Code: 200

for json data

```json
{
"data": {
  "start_time": "01/12/20",
  "end_time": "01/17/20",
  "countries":
  [{"country": "US",
  "confirmed": 300400,
  "recovered": 123000,
 },
  {"country": "Canada",
  "confirmed": 340000,
  "recovered": 1000,
  }]
	}
}
```

- [x] for csv data

```

```

**Error Response**

Code: 400

Code: 

