from .AbstractTableDAO import AbstractTableDAO


class FamilyDAO(AbstractTableDAO):
    def __init__(self):
        super().__init__("family")

    def add_family(self, name, squad_id):
        sql = f"INSERT INTO {self.table_name} (name, squad_id) VALUES (%s, %s)"
        parameters = (name, squad_id)
        self._execute(sql, parameters=parameters, commit=True)
        return True


