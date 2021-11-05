import os
import urllib.parse as urlparse
import psycopg2


def setup_db():
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
        db = "dbname=csc301_a2 user=morganchang password="
        conn = psycopg2.connect(db)
    return conn
    # cur = conn.cursor()


# env = os.environ.get('PYTHON_ENV')
# if env == "production":
#     url = urlparse.urlparse(os.environ['DATABASE_URL'])
#     dbname = url.path[1:]
#     user = url.username
#     password = url.password
#     host = url.hostname
#     port = url.port
#     # db = "dbname=%s user=%s password=%s host=%s" % (url.path[1:], url.username, url.password, url.hostname)
#     conn = psycopg2.connect(
#         dbname=dbname,
#         user=user,
#         password=password,
#         host=host,
#         port=port
#     )
# else:
#     db = "dbname=csc301_a2 user=morganchang password="
#     conn = psycopg2.connect(db)
# cur = conn.cursor()

# '''
#     drops the database tables and starts fresh
#     can be used to initialize a clean database
# '''
# def db_drop_and_create_all():
#     db.drop_all()
#     db.create_all()
