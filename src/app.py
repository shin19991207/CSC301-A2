import os

from flask import Flask
from routes.daily_reports import daily_reports
from routes.time_series import time_series


app = Flask(__name__)

app.register_blueprint(daily_reports, url_prefix='/daily_reports', debug=True)
app.register_blueprint(time_series, url_prefix='/time_series', debug= True)


@app.route("/")
def hello():
    env = os.environ.get('PYTHON_ENV')
    if env == "production":
        return "Production environment"
    else:
        return "Development environment"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
