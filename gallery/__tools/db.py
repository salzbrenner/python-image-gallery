# import psycopg2
# import json
# from .secrets import get_secret_image_gallery
#
# connection = None
#
#
# def get_secret():
#     return json.loads(get_secret_image_gallery())
#
#
# def get_password(secret):
#     return secret['password']
#
#
# def get_host(secret):
#     return secret['host']
#
#
# def get_username(secret):
#     return secret['username']
#
#
# def connect():
#     global connection
#     secret = get_secret()
#     connection = psycopg2.connect(
#         host=get_host(secret),
#         dbname=get_username(secret),
#         user=get_username(secret),
#         password=get_password(secret)
#     )
#
#
# def execute(query, dynamic_vars=None):
#     global connection
#     cursor = connection.cursor()
#     if dynamic_vars:
#         cursor.execute(query, dynamic_vars)
#     else:
#         cursor.execute(query)
#     return cursor
#
#
# def save():
#     global connection
#     connection.commit()
#
#
# def get_users():
#     res = execute('select * from users;')
#     return res
#
#
# def get_single_user(username):
#     res = execute("""
#                     select *
#                     from users u
#                     where u.username = %s;
#                     """,
#                   (username,))
#
#     if res.rowcount == 0:
#         return None
#
#     for row in res:
#         return row
#
#
# def add_user(username, pw, full_name):
#     if not get_single_user(username):
#         execute("insert into users values (%s, %s, %s);",
#                 (username, pw, full_name))
#         save()
#         return True
#     return False
#
#
# def edit_user(username, pw, full_name):
#     user = get_single_user(username)
#
#     if not user:
#         return False
#
#     new_pass = user[1]
#     new_name = user[2]
#
#     if pw:
#         new_pass = pw
#
#     if full_name:
#         new_name = full_name
#
#     execute("""
#     update
#     users
#     set
#     username=%s, password=%s, full_name=%s
#     where username=%s;""",
#             (username, new_pass, new_name, username))
#     save()
#     return True
#
#
# def delete_user(username):
#     user = get_single_user(username)
#
#     if not user:
#         return False
#
#     execute("""
#     delete from users u
#     where u.username = %s;
#     """, (username,))
#     save()
#     return True
#
#
# def main():
#     connect()
#     res = execute('select * from users;')
#
#     for row in res:
#         print(row)
#
#
# if __name__ == '__main__':
#     main()
