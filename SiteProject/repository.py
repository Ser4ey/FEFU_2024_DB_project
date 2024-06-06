import psycopg2

from dto import InsectDTO


class Repository:
    def __init__(self):
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

    def get_all_insects(self):
        sql = """
        SELECT
        insect.id AS insect_id,
        lat_name,
        ru_name,
        img,
        
        squad.id AS squad_id,
        squad.name AS squad_name,
        family.id AS family_id,
        family.name AS family_name,

        description,
        category_and_status,
        distribution,
        area, 
        habitat, 
        limiting_factors,
        count_ AS count,
        security_notes 
        
        FROM insect 
            JOIN family ON insect.family_id = family.id
            JOIN squad ON family.squad_id = squad.id;
        """
        insects = self._execute(sql, fetchall=True)
        return [InsectDTO(*insect) for insect in insects]

    def get_insect(self, id_: int):
        sql = """
        SELECT
        insect.id AS insect_id,
        lat_name,
        ru_name,
        img,

        squad.id AS squad_id,
        squad.name AS squad_name,
        family.id AS family_id,
        family.name AS family_name,

        description,
        category_and_status,
        distribution,
        area, 
        habitat, 
        limiting_factors,
        count_ AS count,
        security_notes 

        FROM insect 
            JOIN family ON insect.family_id = family.id
            JOIN squad ON family.squad_id = squad.id
        
        WHERE insect.id = %s;
        """
        parameters = (id_, )
        insect = self._execute(sql, parameters, fetchone=True)
        print(insect)
        return InsectDTO(*insect)


if __name__ == "__main__":
    r = Repository()
    print(r.get_all_insects()[0])

