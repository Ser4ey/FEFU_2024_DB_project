import re
import time

from repository import InsectDAO, SquadDAO, FamilyDAO
from parsers import CiconParser, RuwikiParser, AbstractInsectParser


class DB_DAO:
    def __init__(self):
        self.insect_dao = InsectDAO()
        self.family_dao = FamilyDAO()
        self.squad_dao = SquadDAO()

        self.all_insect = {}
        self.all_family = {}
        self.all_squad = {}
        self.init_dicts()

        print(f"Насекомые в бд: {self.all_insect}")
        print(f"Семейства в бд: {self.all_family}")
        print(f"Отряды в бд: {self.all_squad}")

    def init_dicts(self):
        insects = self.insect_dao.select_all()
        for i in insects:
            self.all_insect[i[0]] = i

        families = self.family_dao.select_all()
        for i in families:
            self.all_family[i[0]] = i

        squads = self.squad_dao.select_all()
        for i in squads:
            self.all_squad[i[0]] = i

    def update_db(self, insect_parser: AbstractInsectParser):
        links = insect_parser.get_insects_links()

        for i in range(len(links)):
            print(f"Ссылка {i+1}/{len(links)}")
            insect_info = insect_parser.get_insect(links[i])
            print(insect_info)

            self.add_and_update_insect(insect_info)
            print(f"Насекомое успешно добавлена в бд\n")

    def add_and_update_insect(self, insect_info: dict):
        lat_name = insect_info["lat_name"]
        ru_name = insect_info["ru_name"]

        squad = insect_info["squad"]
        family = insect_info["family"]

        if (not lat_name) or (not ru_name) or (not squad) or (not family):
            print(f"Нет ключевой информации о насекомом: {insect_info}")
            return

        update_kwargs = {}
        for key, value in insect_info.items():
            if (not (key in ["lat_name", "ru_name", "squad", "family"])) and not value.strip():
                update_kwargs[key] = value

        self.add_to_db_if_not_exist(lat_name, ru_name, squad, family)

    def add_to_db_if_not_exist(self, lat_name: str, ru_name: str, squad_name: str, family_name: str):
        squad = self.squad_dao.select_one(name=squad_name)
        if squad is None:
            self.squad_dao.add_squad(squad_name)
            squad = self.squad_dao.select_one(name=squad_name)

        squad_id = squad[0]
        print(squad, squad_id)
        #
        # self.squad_dao.add_squad(squad)
        #
        # squad_id = self.squad_dao.select_one(name=squad)[0]
        # print(squad_id, squad)





if __name__ == "__main__":
    db_dao = DB_DAO()

    db_dao.update_db(CiconParser())


