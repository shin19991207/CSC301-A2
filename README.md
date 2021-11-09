# CSC301 Assignment 2

## Pair Programming

* Yanling (driver), Morgan (navigator)
  * **Feature**: Design inputs and outputs of the API 
    * Yanling worked as a driver when writing the rough draft of the API documentation, but we discussed together to figure out inputs that are necessery to meet the required functionalities and also optional inputs that are not essential but enable users to customize the output of the API. 
    * Even though the description of main functionalities are given but there are still a lot of flexibilities in the implementation. The file can be uploaded in several ways through the requests and the design of the endpoints are required as we need to handle two distinct types of tiles. Besides, even though the sample inputs are given, we need to descide which set of inputs are necessary and which are not so essential. Also, some features can be implemented multiple ways. For example, if users give a start_date and end_date, we can either return users the total number of people they are interested in or return a list of numbers wherer one value corresponds to information on one day. 
    * I (Yanling) enjoy discussing with my partner to figure out the users' needs and detailed implementations, since a clear understanding of users' needs and the process of thinking detailed implemetation make us to implemente the features efficiently without changing back and forth due to bad understanding of the project requirements. Also, we can divide the tasks easily and then finish the assignment faster.
  * **Feature**: Load csv file to relational PostgreSQL database
    * Yanling and Morgan search around the postman and read posts in Piazza to find out a way to send data through post requests and then load data from requests to PostgreSQL database. After a series of trials, we reach an agreement and Morgan as a driver wrote codes to read in file from users' requests and then the role is switched and Yanling is then driver to load data to the postgreSQL, whereas Morgan as a navigator is ready to discuss any error encounter when loading the database
    * Our largest challenge is that the relational database like postgreSQL restrict hard on data to load and thus when the column titles and values contain special characters such as single quote, black slash and comma, we fail to load data to database and thus clearful handling is needed.
    * I (Yanling) like this part of the pair programming since having someone to discuss makes the debugging tolerable and more efficient. It is commons that I made a tiny mistake which results in a failure to load database. Usually, we found the error either immediately or  within several minutes of discussing and if the problem is so hard that we can't solve immediately, we searched around symotaneously and often it speeds up our debugging process.


* Morgan (driver), Yanling (navigator)

  * **Feature**: Query data
    * 
  * **Feature**:  Writing unit tests
    * I (Morgan) was a driver when writing the unit test and debugging the code functionality of our program. The debugging step is always a tough process in writing a program, since it is often the codes that you are confident with that cause the error. The pair programming process went quite well and faster the pace of debugging. When an error arose in our program or a feature did not work, the navigator (my parter) would ask me to explain my code line by line to her. Often, through the procedure of justifying each line of code and conveying my initial thought on doing these steps, I could find out what and where went wrong by myself, or my partner would point out the steps that she found unworkable.
    * **Challenge**: Writing unit test and debugging code functionality
    * Reflection: I enjoyed doing pair programming with my partner as it was more productive than if I was debugging alone. Such a process helps me to find out what and where went wrong more efficiently, although it was sometimes hard to understand the changes navigator want me to make by just having her telling me the code or the functions and modules to use orally. 

## Program design

### Design Decisions

 * We supports only files of **global** data to be added or uploaded to our program. Since our program checks if a file is in the correct format when the user tries to upload a data file, we need the uploaded files to be in a consistent format. Since the global and US data files are formatted differently, we choose to support only data files in the **global** data format.
 * We use Heroku Postgres to store the uploaded data from user. Since there is an enforced row limits of 10,000 rows in our database, please be aware of the rows in each data file uploaded.
 * We make decision on the maximum number of data files that can be saved to our program according to the limitations of our database used mentioned above. Since each global daily report contains approximately 5000 rows, we can allow at most and only one daily report to exist in or to be saved into our database. Each global time series data file contains approximately 300 rows, so we decided to allow at most 4 time series data to exist in or to be saved into our database, reserving one slot for each case type.

### Design Patterns
 * [X] mention some design patterns here


## Functionality

* **Adding a new data file**: The user can upload a csv file to our API using the endpoints `/time_series/data?type={type}` for time series data and `/daily_reports/data` for daily_reports data. Only one file can be sent at a time and the uploading time takes about 10 seconds.

  * Time Series Data (`/time_series/data?type={type}`):
    * The file format should be consistent and follows the format of `time_series_covid19_{type}_global.csv` specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series). Note that our program only accepts the format of **global** time series data, that is, any files with the format of `time_series_covid19_{type}_US.csv` will not be accepted and will cause an error response with code 400.
    * `type` param in the url endpoint should be one of `confirmed`, `deaths`, `recovered`, or `active`.
    
  * Daily Reports Data (`/daily_reports/data`):
    * The file format should be consistent and follows the format of the **global** daily reports specified [here](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports). Note that files formatted as US daily reports are not accepted and will cause an error response with code 400.
  
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
    * The user can only query data on the date of the most recent-uploaded daily report.

* **Support returning the data in multiple formats: json and csv**
  * Our program supports returning data in `JSON` and `CSV`.
  

## Instructions 

### Setup for Running on a Local Machine

* Our program is compatible with and tested on Mac OS. If running locally, please note that the program might not be compatible with and is not guaranteed to be able to run on any other operating systems, including Ubuntu Linux, since some required packages or packages version specified in `requirements.txt` is not supported on specific os.
* To ensure proper configuration while running on a local machine, ensure that you follow the following steps:

1. `git clone https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207.git && cd assignment-2-61-yanling-h-shin19991207`

2. A `.env` file is required for environment variables and requires the following variables to be defined. Note that this file must be placed in the src root directory `src/.env`

  ```
  DB_NAME=<database name>
  DB_USER=<username for accessing database>
  ```

 3. Create a virtualenv named `venv` using `$ python3 -m venv venv`
 4. Activate the virtualenv using `$ source venv/bin/activate`
 5. Install the required libraries from `pip` using `$ pip3 install -r requirements.txt`
 6. Run the API using `$ python3 src/app.py`
 7. This should get our API running on http://localhost:5000/. Calls can be made according to the [REST-API-Documentation](#rest-api-documentation) on the root url.

### Accessing the API Online

The API is deployed to https://covid-monitor-61.herokuapp.com/ and calls can be made according to the [REST-API-Documentation](#rest-api-documentation).

### Recommeded Steps for Using the API
Follow the recommeded steps for using the API to prevent from error responds.

* **Time Series**
 1. Upload global time series data from endpoint `/time_series/data?type={type}`

* **Daily Reports**


## Tests

### Unittest

* We design unit tests to test our code functionality for the util functions and routers. 
* We set up a small test table in our Heroku Postgres database to test the behaviors and functionalities related to databases in `utils.py`. 
* We test the routers by sending requests in expected format and check if the respond is successful.
* We have 88% line coverage in the most recent test as shown [here](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/main/docs/test_coverage.png) and below.

 ```
 $ coverage run -m unittest         
 .........
 ----------------------------------------------------------------------
 Ran 9 tests in 5.732s

 OK

 $ coverage report -m       
 Name                                 Stmts   Miss  Cover   Missing
 ------------------------------------------------------------------
 src/__init__.py                          0      0   100%
 src/config.py                           20      7    65%   12-19
 src/routes/__init__.py                   0      0   100%
 src/utils.py                            87     12    86%   26, 81, 86-88, 100-102, 106, 109-111
 tests/__init__.py                        2      0   100%
 tests/routes/__init__.py                 0      0   100%
 tests/routes/test_daily_reports.py      18      1    94%   44
 tests/routes/test_time_series.py        18      1    94%   37
 tests/test_utils.py                     47      3    94%   64-65, 114
 ------------------------------------------------------------------
 TOTAL                                  192     24    88%
 ```

### Continuous Integration

* We set up [CI](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/main/.github/workflows/unittest.yml) with Github Actions to run our unit test each time we make changes on the [main branch](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/tree/main).


## REST API Documentation

### Endpoints

* [Load Time Series Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/main/docs/load_daily_reports.md)
* [Query Time Series Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/main/docs/query_time_series.md)
* [Load Daily Reports Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/main/docs/load_daily_reports.md)
* [Query Daily Reports Data](https://github.com/csc301-fall-2021/assignment-2-61-yanling-h-shin19991207/blob/main/docs/query_daily_reports.md)

