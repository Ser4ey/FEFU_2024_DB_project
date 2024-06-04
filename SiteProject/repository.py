import psycopg2


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
            JOIN squad ON family.squad_id = squad.id
        """
        insects = self._execute(sql, fetchall=True)
        return [Insect(*insect) for insect in insects]


class Insect:
    def __init__(self, insect_id, lat_name, ru_name, img, squad_id, squad_name, family_id, family_name, description, category_and_status, distribution, area, habitat, limiting_factors, count, security_notes):
        self.insect_id = insect_id
        self.lat_name = lat_name
        self.ru_name = ru_name
        self.img = img
        self.squad_id = squad_id
        self.squad_name = squad_name
        self.family_id = family_id
        self.family_name = family_name
        self.description = description
        self.category_and_status = category_and_status
        self.distribution = distribution
        self.area = area
        self.habitat = habitat
        self.limiting_factors = limiting_factors
        self.count = count
        self.security_notes = security_notes

    def __str__(self):
        return f"Insect {self.lat_name} (ID: {self.insect_id}) - {self.family_name} ({self.squad_name})"


if __name__ == "__main__":
    r = Repository()
    print(r.get_all_insects()[0])