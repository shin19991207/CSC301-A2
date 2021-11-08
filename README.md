# CSC301 Assignment 2

## Pair Programming

* Yanling (driver), Morgan (navigator)
  * Challenge: 
  * Reflection:

* Morgan (driver), Yanling (navigator)
  * Challenge: 
  * Reflection:

## Program design



## Functionality

* **Adding a new data file**: The user can upload a csv file to our API using the endpoints `/time_series/data?type={type}` for time series data and `/daily_reports/data` for daily_reports data.

* **Update existing files**
* **Query data**
* **Support returning the data in multiple formats: json and csv**


## Instructions 

### Setup

#### Running on Local Machine

To ensure proper configuration while running on a local machine, ensure that you follow the following steps:

1. A `.env` file is required for environment variables and requires the following variables to be defined. Note that this file must be placed in the src root directory as `.env`

  ```
  DB_NAME=<database name>
  DB_USER=<username for accessing database>
  ```
  
 2. Create a virtualenv named `venv` using `$ python3 -m venv venv`
 3. Activate the virtualenv using `$ source venv/bin/activate` (Mac OS & Linux)
 4. Install the required libraries from `pip` using `$ pip install -r requirements.txt`
 5. Run the API using `$ python3 src/app.py`
 6. This should get our API running on http://localhost:5000/. Calls can be made according to the [REST-API-Documentation](#rest-api-documentation) on the root url.

#### Accessing the API Online

The API is deployed to https://covid-monitor-61.herokuapp.com/ and calls can be made according to the [REST-API-Documentation](#rest-api-documentation).


## Tests


## REST API Documentation

### Endpoints

* [Load Time Series Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/load_time_series.md)
* [Query Time Series Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/query_time_series.md)
* [Load Daily Reports Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/load_daily_reports.md)
* [Query Daily Reports Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/query_daily_reports.md)
