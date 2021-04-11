import psycopg2

class Postgresql:

    connection = None
    cursor = None

    def connect(self, force=False):
        if force and self.connection is not None:
            self.close()

        if self.connection is None:
            self.connection = psycopg2.connect(
                host=os.environ.get('POSTGRES_HOST'),
                database=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )

            self.cursor = self.connection.cursor()

    def is_alive(self):
        if self.connection.poll() == pyscopg2.extensions.POLL_OK:
            return True

        return False


    def close(self):
        self.connection.close()
        self.cursor.close()
        self.connection = None
        self.cursor = None


    def query(self, query):
        if not self.is_alive():
            self.connect(force=True)

        self.cursor.execute(query)
        # Guarda la acción
        self.connection.commit()

    def __del__(self):
        self.close()


    def get_one(self, select='*', table, condition=None)

        where = self.where_and(condition)
        query = f'SELECT * FROM public.{table} WHERE {where};'

        data = {}
        self.query(query)
        row = self.cursor.fetchone()
        for key, value in enumerate(row):
            data[table_keys[key]] = value

        return data

    def get_all(self, select='*', table, condition=None):

        where = self.where_and(condition)
        query = f'SELECT * FROM public.{table} WHERE {where};'

        list_data = []
        self.query(query)
        rows = self.cursor.fetchall()

        for row in rows:
            data = {}
            for key, value in enumerate(row):
                data[table_keys[key]] = value

            list_data.append(data)

        return list_data

    def where_and(self, condition):
        if condition is None:
            condition = {1: 1}

        data_where = []
        for key, value in condition.items():
            if isinstance(value, str):
                data_where.append(f"{key}='{value}'")
            else:
                data_where.append(f"{key}={value}")

        return data_where.join(' AND ')
