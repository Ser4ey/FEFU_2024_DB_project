import psycopg2


class PostgresDB:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="scrapper",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
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

    def add_insect(self, name):
        sql = "INSERT INTO insect (name) VALUES (%s)"
        parameters = (name, )
        self.execute(sql, parameters=parameters, commit=True)
        return True

    def select_all(self):
        sql = 'SELECT * FROM insect'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        # используется для создания sql команды с нужными параметрами для команды ниже
        sql += ' AND '.join([
            f"{item} = %s" for item in parameters.keys()
        ])
        return sql, tuple(parameters.values())

    def select_one(self, **kwargs):
        sql = 'SELECT * FROM insect WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
        # пример использования команды select_desk(id=131, name='JoJo')

    def is_exist(self, id_):
        sql = 'SELECT EXISTS(SELECT 1 FROM insect WHERE id = %s)'
        parameters = (id_, )

        r = self.execute(sql, parameters, fetchone=True)
        return r[0]

    # def count_passwords(self):
    #     # return int(self.execute("SELECT COUNT(*) FROM Columns;", fetchone=True))
    #     return self.execute("SELECT COUNT(*) FROM insect;", fetchone=True)[0]
    #
    # def update_password(self, password_id, new_password):
    #     sql = f"UPDATE insect SET password=? WHERE id=?"
    #     self.execute(sql, parameters=(new_password, password_id), commit=True)
    #     return


if __name__ == '__main__':
    a1 = PostgresDB()

    r = a1.is_exist(5)
    print(r)

    # a1.add_insect("Ant")

    # print(
    #     a1.select_all()
    # )
    # print(a1.select_one(name="werer"))
    # print(a1.select_one(name="Ant"))


def save_to_postgres(data_dict):
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="your_database",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )

    # Создание курсора
    cur = conn.cursor()

    # Создание таблицы, если она не существует
    cur.execute("""
        CREATE TABLE IF NOT EXISTS your_table (
            id SERIAL PRIMARY KEY,
            lat_name TEXT,
            ru_name TEXT,
            img TEXT,
            squad TEXT,
            family TEXT,
            category_and_status TEXT,
            distribution TEXT,
            habitat TEXT,
            limiting_factors TEXT,
            count TEXT,
            security_notes TEXT
        )
    """)

    # Формирование запроса для вставки данных
    insert_query = """
        INSERT INTO your_table (lat_name, ru_name, img, squad, family, category_and_status, distribution, habitat, limiting_factors, count, security_notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Вставка данных в таблицу
    cur.execute(insert_query, (
        data_dict["lat_name"],
        data_dict["ru_name"],
        data_dict["img"],
        data_dict["squad"],
        data_dict["family"],
        data_dict["category_and_status"],
        data_dict["distribution"],
        data_dict["habitat"],
        data_dict["limiting_factors"],
        data_dict["count"],
        data_dict["security_notes"]
    ))

    # Фиксация изменений
    conn.commit()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

# # Пример использования функции
# data = {
#     "lat_name": "lat_name_value",
#     "ru_name": "ru_name_value",
#     "img": "img_value",
#     "squad": "squad_value",
#     "family": "family_value",
#     "category_and_status": "category_and_status_value",
#     "distribution": "distribution_value",
#     "habitat": "habitat_value",
#     "limiting_factors": "limiting_factors_value",
#     "count": "count_value",
#     "security_notes": "security_notes_value"
# }
#
# save_to_postgres(data)