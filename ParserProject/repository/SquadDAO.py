from .AbstractTableDAO import AbstractTableDAO


class SquadDAO(AbstractTableDAO):
    def __init__(self):
        super().__init__("squad")

    def add_squad(self, name):
        sql = f"INSERT INTO {self.table_name} (name) VALUES (%s)"
        parameters = (name, )
        self._execute(sql, parameters=parameters, commit=True)
        return True


