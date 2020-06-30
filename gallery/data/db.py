from ..aws.secrets import get_secret_image_gallery
import psycopg2
import json

secret = json.loads(get_secret_image_gallery())


def connect():
    return psycopg2.connect(
        host=secret['host'],
        dbname=secret['username'],
        user=secret['username'],
        password=secret['password']
    )
