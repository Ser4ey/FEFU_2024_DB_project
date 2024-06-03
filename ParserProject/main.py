from repository import InsectDAO, SquadDAO, FamilyDAO
from parsers import CiconParserClass, RuWikiParserClass, AbstractInsectParser


class DB_DAO:
    def __init__(self):
        self.insect_dao = InsectDAO()
        self.family_dao = FamilyDAO()
        self.squad_dao = SquadDAO()

    def update_db(self, insect_parser: AbstractInsectParser):
        links = insect_parser.get_insects_links()

        for i in range(len(links)):
            print(f"Ссылка {i + 1}/{len(links)}")
            insect_info = insect_parser.get_insect(links[i])
            print(insect_info)

            self.add_and_update_insect(insect_info)
            print(f"Насекомое успешно обновлено в бд\n")

    def add_and_update_insect(self, insect_info: dict):
        lat_name = insect_info["lat_name"]
        ru_name = insect_info["ru_name"]

        squad = insect_info["squad"]
        family = insect_info["family"]

        if (not lat_name) or (not ru_name) or (not squad) or (not family):
            print(f"[-] Нет ключевой информации о насекомом: {insect_info}")
            return

        update_kwargs = {}
        for key, value in insect_info.items():
            print(key, value)
            if (not (key in ["lat_name", "ru_name", "squad", "family"])) and value.strip():
                update_kwargs[key] = value

        self.add_to_db_if_not_exist(lat_name, ru_name, squad, family)

        insect = self.insect_dao.select_one(lat_name=lat_name)
        if not (insect is None):
            print(f"[+] Обновляем инфо о насекомом: {lat_name}")
            print(f"[*] Update info: {update_kwargs}")
            self.update_insect(lat_name=lat_name, update_kwargs=update_kwargs)
        else:
            print(f"[-] Насекомое не найдено: {lat_name}")

    def add_to_db_if_not_exist(self, lat_name: str, ru_name: str, squad_name: str, family_name: str):
        squad = self.squad_dao.select_one(name=squad_name)
        if squad is None:
            self.squad_dao.add_squad(squad_name)
            squad = self.squad_dao.select_one(name=squad_name)
            print(f"[+++] Добавлен новый squad: {squad}")

        squad_id = squad[0]
        print(f"[*] Отряд насекомого: {squad_id} | {squad}")

        family = self.family_dao.select_one(name=family_name)
        if family is None:
            self.family_dao.add_family(name=family_name, squad_id=squad_id)
            family = self.family_dao.select_one(name=family_name)
            print(f"[+++] Добавлен новый family: {family}")

        family_id = family[0]
        print(f"[*] Семейство насекомого: {family_id} | {family}")

        insect = self.insect_dao.select_one(lat_name=lat_name)
        insect_ru = self.insect_dao.select_one(ru_name=ru_name)
        if (insect is None) and (insect_ru is None):
            try:
                self.insect_dao.add_insect(lat_name=lat_name, ru_name=ru_name, family_id=family_id)
                insect = self.insect_dao.select_one(lat_name=lat_name)
                print(f"[+++] Добавлено новое насекомое: {insect}")
            except Exception as er:
                print(f"[---] Не удалось добавить насекомое: {lat_name}. er: {er}")

    def update_insect(self, lat_name, update_kwargs: dict):
        print(f"[+] Обновляем информацию о {lat_name} | {update_kwargs}")
        if not update_kwargs:
            print(f"[*] Нет информации о {lat_name}. update_kwargs: {update_kwargs}")
            return

        insect = self.insect_dao.select_one(lat_name=lat_name)
        insect_id = insect[0]
        self.insect_dao.update_insect(id_=insect_id, **update_kwargs)


if __name__ == "__main__":
    db_dao = DB_DAO()

    db_dao.update_db(CiconParserClass())
    db_dao.update_db(RuWikiParserClass())
