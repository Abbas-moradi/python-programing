import psycopg2

class DatabaseManager:
    def __init__(self, *args, **kwargs):
        self.kwoptions = kwargs
        self.options = args

    def __enter__(self):
        self.conn = psycopg2.connect(*self.options, **self.kwoptions)
        self.curs = self.conn.cursor()
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.curs.close()
        self.conn.close()

with DatabaseManager(dbname='dvdrental', user='postgres') as cursor:
    cursor.execute('SELECT * FROM customer;')
    print(cursor.fetchall())
    
