from abc import ABC

import psycopg2


class AbstractTableDAO(ABC):
    def __init__(self, table_name: str):
        self.table_name = table_name

        self.connection = psycopg2.connect(
            dbname="scrapper",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

    def _execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        # connection.set_trace_callback(logger)
        cursor = self.connection.cursor()
        cursor.execute(sql, parameters)
        data = None

        if commit:
            self.connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        # self.connection.close()

        return data

    def select_all(self):
        sql = f'SELECT * FROM {self.table_name}'
        return self._execute(sql, fetchall=True)

    @staticmethod
    def _format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = %s" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_one(self, **kwargs):
        sql = f'SELECT * FROM {self.table_name} WHERE '
        sql, parameters = self._format_args(sql, kwargs)
        return self._execute(sql, parameters, fetchone=True)
        # пример использования команды select_desk(id=131, name='JoJo')

    def select_many(self, **kwargs):
        sql = f'SELECT * FROM {self.table_name} WHERE '
        sql, parameters = self._format_args(sql, kwargs)
        return self._execute(sql, parameters, fetchall=True)

    def is_exist(self, id_):
        sql = f'SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE id = %s)'
        parameters = (id_, )

        r = self._execute(sql, parameters, fetchone=True)
        return r[0]

    def count(self):
        return self._execute(f"SELECT COUNT(*) FROM {self.table_name};", fetchone=True)[0]


