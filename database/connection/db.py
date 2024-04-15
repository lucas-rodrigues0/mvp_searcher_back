from database.connection.connect import connect


class Db:
    def __init__(self):
        self.conn = connect()
        self.error = None

    def execute(self, command):
        cursor = self.conn.cursor()
        try:
            cursor.execute(command)
            self.conn.commit()
        except Exception as err:
            self.error = f"error: {err}"
            self.conn.rollback()
        finally:
            if self.error:
                cursor.close()
                return self.error
            else:
                cursor.close()
                return "Command executed succesfully!"

    def conn_close(self):
        self.conn.close()
