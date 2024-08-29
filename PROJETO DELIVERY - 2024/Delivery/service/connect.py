import psycopg2

class Connect:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname = "Delivery",
            user="postgres",
            password="admin",
            host="localhost", port="5432"
        )

    def get_instance(self):
        return self.connection