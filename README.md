# CSC301 Assignment 2

## Pair Programming

## Program design

## Functionality

## Instructions 

### Setup

#### Running on Local Machine

To ensure proper configuration while running on a local machine, ensure that you follow the following steps:

1. A .env file is required for environment variables and requires the following variables to be defined. Note that this file must be placed in the src root directory  `backend/.env`

  ```
  DB_NAME=<database name>
  DB_USER=<username for accessing database>
  ```

2. Install the required libraries from `pip` using `$ pip install -r requirements.txt`
3. Run the API using `$ python3 src/app.py`

#### Accessing the API Online

The API is deployed to https://covid-monitor-61.herokuapp.com/ and calls can be made according to the [REST-API-Documentation](#REST API Documentation
).


## Tests


## REST API Documentation

### Endpoints

* [Load Time Series Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/load_time_series.md)
* [Query Time Series Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/query_time_series.md)
* [Load Daily Reports Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/load_daily_reports.md)
* [Query Daily Reports Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/develop/docs/query_daily_reports.md)
