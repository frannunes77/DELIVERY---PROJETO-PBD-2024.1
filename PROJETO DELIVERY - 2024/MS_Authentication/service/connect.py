import psycopg2

class Connect:

    def __init__(self):
        self._connection = psycopg2.connect(
        dbname="MS_Authentication",
        user="postgres",
        password="admin",
        host="localhost", port="5432"
)

    def get_instance(self):
        return self._connection
