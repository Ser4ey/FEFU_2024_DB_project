from .AbstractTableDAO import AbstractTableDAO


class InsectDAO(AbstractTableDAO):
    def __init__(self):
        super().__init__("insect")

    def add_insect(self, lat_name: str, ru_name: str, family_id: int):
        sql = f"INSERT INTO {self.table_name} (lat_name, ru_name, family_id) VALUES (%s, %s, %s)"
        parameters = (lat_name, ru_name, family_id)
        self._execute(sql, parameters=parameters, commit=True)
        # print("id: ", a)

    @staticmethod
    def _format_args_to_update(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' , '.join([
            f"{item} = %s" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_one(self, **kwargs):
        sql = f'SELECT * FROM {self.table_name} WHERE '
        sql, parameters = self._format_args(sql, kwargs)
        return self._execute(sql, parameters, fetchone=True)
        # пример использования команды select_desk(id=131, name='JoJo')

    def update_insect(self, id_, **kwargs):
        sql = f'UPDATE {self.table_name} SET '
        sql, parameters = self._format_args_to_update(sql, kwargs)
        sql += " WHERE id = %s"
        parameters = parameters + (id_, )
        # print(parameters)
        # print(sql)

        self._execute(sql, parameters=parameters, commit=True)

