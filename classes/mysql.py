import mysql.connector
import os
import time

class Mysql:

    mydb = None
    cursor = None

    def __init__(self):
        self.connect()


    def connect(self):

        if self.mydb is None or not self.mydb.is_connected():
            try:
                self.mydb = mysql.connector.connect(
                    host=os.environ.get('MYSQL_HOST'),
                    user=os.environ.get('MYSQL_USER'),
                    password=os.environ.get('MYSQL_PASS'),
                    database=os.environ.get('MYSQL_DB'),
                    port=os.environ.get('MYSQL_PORT'),
                )

                self.cursor = self.mydb.cursor()
            except mysql.connector.Error as err:
                print(err)
                time.sleep(3)
                print('Retry connect...')
                self.connect()

        print('Database connection succesfully')


    def __del__(self):
        print('Close connection')
        self.close()

    def close(self):
        if self.mydb is None:
            return
        self.mydb.close()

    def launch_query(self, query):

        if not self.mydb.is_connected():
            self.connect()
        print(query)

        try:
            self.cursor.execute(query)
        except Exception as err:
            print(err)


    def insert_data(self, table, data):

        values = "'" + "', '".join(data.values()) + "'"
        query = f'INSERT INTO {table} ({", ".join(data.keys())}) VALUES ({values});'
        self.launch_query(query)

        self.mydb.commit()

        if self.cursor.rowcount > 0:
            return self.cursor.lastrowid
        else:
            return None

    def update_data(self, table, data, condition):

        fields_to_update = []
        for field_name, field_value in data.items():
            fields_to_update.append(f"{field_name}='{field_value}'")

        where = self.where_and(condition)

        query = f'UPDATE {table} SET {", ".join(fields_to_update)} WHERE {where};'

        self.launch_query(query)
        self.mydb.commit()

        if self.cursor.rowcount > 0:
            return True
        else:
            return False


    def where_and(self, condition):
        if condition is None:
            condition = {1: 1}

        data_where = []
        for key, value in condition.items():
            data_where.append(f'{key}="{value}"')

        return data_where.join(' AND ')

    def get_all(self, table, select='*', condition='1=1'):

        where = condition
        if type(condition) == dict:
            where = where_and(condition)

        query = f'SELECT {select} FROM {table} WHERE {where}'
        self.launch_query(query)

        rows = self.cursor.fetchall()

        list_data = []

        for row in rows:
            data = {}
            for key, value in enumerate(row):
                data[key] = value

            list_data.append(data)

        return list_data

    def get_one(self, table, select='*', condition='1=1'):
        where = condition
        if type(condition) == dict:
            where = where_and(condition)

        query = f'SELECT {select} FROM {table} WHERE {where}'
        self.launch_query(query)

        row = self.cursor.fetchone()
        data = {}
        for key, value in enumerate(row):
            data[table_keys[key]] = value

        return data

