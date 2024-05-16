from .AbstractTableDAO import AbstractTableDAO


class InsectDAO(AbstractTableDAO):
    def __init__(self):
        super().__init__("insect")

    def add_insect(self, name):
        sql = f"INSERT INTO {self.table_name} (name) VALUES (%s)"
        parameters = (name, )
        self._execute(sql, parameters=parameters, commit=True)
        return True

    def update_insect(self, password_id, new_password):
        sql = f"UPDATE {self.table_name} SET password=? WHERE id=?"
        self._execute(sql, parameters=(new_password, password_id), commit=True)

