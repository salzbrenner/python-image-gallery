import psycopg2
import os


password = os.environ.get('IG_PASSWD')

if os.environ.get('IG_PASSWD_FILE'):
    f = open(os.environ.get('IG_PASSWD_FILE'))
    password = f.readline().rstrip("\n")
    f.close()


def get_db():
    return psycopg2.connect(
        host=os.environ.get('PG_HOST'),
        dbname=os.environ.get('IG_DATABASE'),
        user=os.environ.get('IG_USER'),
        password=password
    )


# def connect():
#     if 'db' not in g:
#         g.db = psycopg2.connect(
#             host='m6-db-1.cbjekp7qkzy2.us-west-1.rds.amazonaws.com',
#             dbname='image_gallery_dev',
#             user='image_gallery',
#             password='where_do_dogs_roam'
#         )
#
#     return g.db
#
#
# def close_db(e=None):
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#
