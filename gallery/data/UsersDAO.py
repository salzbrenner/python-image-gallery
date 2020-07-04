from .User import User
from .BaseDAO import BaseDAO


class UsersDAO(BaseDAO):

    def get_users(self):
        res = self.execute('select * from users;')
        users = []
        for u in res:
            users.append(User(u[0], u[1], u[2]))
        return users

    def get_single_user(self, username):
        res = self.execute("""  
                        select * 
                        from users u 
                        where u.username = %s;
                        """,
                           (username,))

        if res.rowcount == 0:
            return None

        row = res.fetchone()
        return User(row[0], row[1], row[2])

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

        new_pass = user.password
        new_name = user.full_name

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
