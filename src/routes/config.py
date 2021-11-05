from dotenv import load_dotenv

import os
import urllib.parse as urlparse
import psycopg2

load_dotenv()


def connect_database():
    env = os.environ.get('PYTHON_ENV')
    if env == "production":
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        # db = "dbname=%s user=%s password=%s host=%s" % (url.path[1:], url.username, url.password, url.hostname)
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    else:
        db_name = os.environ.get('DB_NAME')
        db_user = os.environ.get('DB_USER')
        db = "dbname=%s user=%s password=" % (db_name, db_user)
        conn = psycopg2.connect(db)
    return conn

