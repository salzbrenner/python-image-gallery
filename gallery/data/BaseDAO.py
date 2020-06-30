class BaseDAO:
    def __init__(self, connection):
        self.connection = connection

    def execute(self, query, dynamic_vars=None):
        cursor = self.connection.cursor()
        if dynamic_vars:
            cursor.execute(query, dynamic_vars)
        else:
            cursor.execute(query)
        return cursor

    def save(self):
        self.connection.commit()