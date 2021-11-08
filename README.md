# CSC301 Assignment 2

## Pair Programming

* Yanling (driver), Morgan (navigator)
  * Challenge: 
  * Reflection:

* Morgan (driver), Yanling (navigator)
  * Challenge: 
  * Reflection:

## Program design

* We use Heroku Postgres to store the uploaded data from user. Since there is an enforced row limits of 10,000 rows in our database, please be aware of the rows in each data file uploaded.


## Functionality

* **Adding a new data file**: The user can upload a csv file to our API using the endpoints `/time_series/data?type={type}` for time series data and `/daily_reports/data` for daily_reports data. Only one file can be sent at a time and the uploading time takes about 10 seconds.

  * Time Series Data (`/time_series/data?type={type}`):
    * The file format should be consistent and follows the format of `time_series_covid19_{type}_global.csv` specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series).
    * `type` param in the url endpoint should be one of `confirmed`, `deaths`, `recovered`, or `active`.
    
  * Daily Reports Data (`/daily_reports/data`):
    * The file format should be consistent and follows the format of the global daily reports specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports).
    * Our program only supports global daily reports format. US daily reports format is not supported.
    
* **Update existing files**: The url endpoint is as same as the one for adding a new data file.

  * Time Series Data (`/time_series/data?type={type}`):
    * Our program can save up to 4 time series data, one for each `type`. If a same `type` of time series data file is uploaded again, the new information will be reflected in our program.

  * Daily Reports Data (`/daily_reports/data`):
    * Our proram can save up to 1 daily report data. If a daily report is uploaded again, the new information will be reflected in our program.

* **Query data**: Our program allows queries for one or more countries/regions and allows any combination of countries/regions, provinces/states, and/or combined key as long as country/region is provided for each. It also allows choosing the cases type to query as long as at least one of the 4 that are available (confirmed, deaths, recovered, active) is provided.

  * Time Series Data (`/time_series/cases`):
    * The user can query data for any range of dates (>= 1 day), as long as the start and end dates provided are in the uploaded time series data.
    * Type `Active` can only be queried when all three other types are all available in our program. 
  
  * Daily Reports Data (`/daily_reports/cases`):
    * The user can only query data with the date of the most recent daily report uploaded.

* **Support returning the data in multiple formats: json and csv**
  * Our program supports returning data in JSON and CSV.
  

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
# a2_cicd
# a2_cicd
