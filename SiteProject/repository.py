import psycopg2

class Repository:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="scrapper",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        self.cur = self.conn.cursor()

    def get_insects(self, limit, offset):
        self.cur.execute("SELECT * FROM insect ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        return self.cur.fetchall()

    def get_insect(self, id):
        self.cur.execute("SELECT * FROM insect WHERE id = %s", (id,))
        return self.cur.fetchone()

    def search_insects(self, squad_id, family_id):
        query = "SELECT * FROM insect"
        if squad_id:
            query += " WHERE family_id IN (SELECT id FROM family WHERE squad_id = %s)" % squad_id
        if family_id:
            query += " WHERE family_id = %s" % family_id
        self.cur.execute(query)
        return self.cur.fetchall()