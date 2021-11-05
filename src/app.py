import os

from flask import Flask
from routes.daily_reports import daily_reports
from routes.time_series import time_series

app = Flask(__name__)
env = os.environ.get("PYTHON_ENV")

app.register_blueprint(daily_reports, url_prefix='/daily_reports')
app.register_blueprint(time_series, url_prefix='/time_series')

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
