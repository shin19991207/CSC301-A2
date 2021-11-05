import os

from flask import Flask
from routes.daily_reports import daily_reports
from routes.time_series import time_series
from models import setup_db

app = Flask(__name__)
env = os.environ.get('PYTHON_ENV')

app.register_blueprint(daily_reports, url_prefix='/daily_reports')
app.register_blueprint(time_series, url_prefix='/time_series')

conn = setup_db()
cur = conn.cursor()
id = 1
cur.execute(f"INSERT INTO testtable VALUES ({id});")
cur.close()
conn.commit()
conn.close()


@app.route("/")
def hello():
    if env == "production":
        return "production"
    else:
        return "Hello World!"


if __name__ == '__main__':
    print(env)
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
