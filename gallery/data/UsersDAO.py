import psycopg2
from ..aws.secrets import get_secret_image_gallery
import json


class UsersDAO():
    def __init__(self):
        secret = json.loads(get_secret_image_gallery())
        self.connection = psycopg2.connect(
            host=secret['host'],
            dbname=secret['username'],
            user=secret['username'],
            password=secret['password']
        )

    def execute(self, query, dynamic_vars=None):
        cursor = self.connection.cursor()
        if dynamic_vars:
            cursor.execute(query, dynamic_vars)
        else:
            cursor.execute(query)
        return cursor

    def save(self):
        self.connection.commit()

    def get_users(self):
        res = self.execute('select * from users;')
        return res

    def get_single_user(self, username):
        res = self.execute("""
                        select * 
                        from users u 
                        where u.username = %s;
                        """,
                           (username,))

        if res.rowcount == 0:
            return None

        for row in res:
            return row

    def add_user(self, username, pw, full_name):
        if not self.get_single_user(username):
            self.execute("insert into users values (%s, %s, %s);",
                         (username, pw, full_name))
            self.save()
            return True
        return False

    def edit_user(self, username, pw, full_name):
        user = self.get_single_user(username)

        if not user:
            return False

        new_pass = user[1]
        new_name = user[2]

        if pw:
            new_pass = pw

        if full_name:
            new_name = full_name

        self.execute("""
            update
            users
            set
            username=%s, password=%s, full_name=%s
            where username=%s;""",
                     (username, new_pass, new_name, username))
        self.save()
        return True

    def delete_user(self, username):
        user = self.get_single_user(username)

        if not user:
            return False

        self.execute("""
            delete from users u
            where u.username = %s;
            """, (username,))

        self.save()
        return True
