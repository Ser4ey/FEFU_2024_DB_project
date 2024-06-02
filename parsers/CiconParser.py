import re
import time

import bs4
import requests
from bs4 import BeautifulSoup

from .AbstractInsectParser import AbstractInsectParser


class CiconParserClass(AbstractInsectParser):
    insects_catalogue_url = "https://cicon.ru/nasekomie.html"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            # 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Host': 'ru.ruwiki.ru',
            # 'Cookie': 'ruwikiRecommendeeId=5e038d17-f3ff-11ee-88eb-005056030e66; ruwikimwuser-sessionId=f04ef1f52053dced4a7f; session-cookie=17c8c67c390915f64f064c3e04983c47c6b3208cc7c2338f7f001f8e46953fd0b526aa5bd218d5aa8189f227f52ed9a6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        }

    def _get(self, url: str) -> str:
        start_time = time.time()
        print(f"Запрос к {url}")
        r = self.session.get(url)
        print(f"Ответ за: {round(time.time()-start_time, 3)}")

        if r.status_code != 200:
            print(f"Error. Status code: {r.status_code} Text: {r.text}")
            exit()
        return r.text

    def get_insects_links(self):
        r = self._get(CiconParserClass.insects_catalogue_url)

        soup = BeautifulSoup(r, 'lxml')
        blocks = soup.select(".lin li a")

        links = []
        for i in range(len(blocks)):
            insect_name = blocks[i].text
            insect_link = blocks[i].get("href")
            link = "https://cicon.ru" + insect_link
            links.append(link)
            print(f"{i+1}) {insect_name} - {link}")

        return links

    def get_insect(self, url: str):
        r = self._get(url)
        soup = BeautifulSoup(r, 'lxml')

        lat_name, ru_name, img, squad, family = self._get_lat_ru_names_and_img_and_squad_family(soup)
        return {
                "lat_name": lat_name,
                "ru_name": ru_name,
                "img": img,

                "squad": squad,
                "family": family,

                "category_and_status": self._get_classification_info(soup, "Категория и статус"),
                # "description": self._get_info_block(soup, "Описание"),
                "distribution": self._get_classification_info(soup, "Распространение"),
                # "area": self._get_classification_info(soup, "Места обитания и особенности экологии"),
                "habitat": self._get_classification_info(soup, "Места обитания и особенности экологии"),
                "limiting_factors": self._get_classification_info(soup, "Лимитирующие факторы"),
                "count_": self._get_classification_info(soup, "Численность"),
                "security_notes": self._get_classification_info(soup, "Принятые меры охраны"),
        }

    @staticmethod
    def contains_cyrillic(text):
        # Регулярное выражение для русских букв в Unicode
        cyrillic_pattern = re.compile('[\u0400-\u04FF]')
        # Проверяем, соответствует ли строка шаблону
        return bool(cyrillic_pattern.search(text))

    def _get_lat_ru_names_and_img_and_squad_family(self, soup: bs4.BeautifulSoup) -> (str, str, str, str, str):
        ru_name = soup.select_one("h1").text

        article = soup.select_one("#content article")

        img = article.find("img").get("src")
        img = "https://cicon.ru" + img

        text = article.find("pre").text
        text = text.split("\n")
        text = [i.strip() for i in text]

        lat_name = " ".join(text[1].split(" ")[:2])

        squad = text[-2].split("–")[0].strip()
        family = text[-1].split("–")[0].strip()

        squad = squad.split()[-1]
        family = family.split()[-1]
        # squad = text[-2].split("–")[-1].strip()
        # family = text[-1].split("–")[-1].strip()
        # if self.contains_cyrillic(squad):
        #     squad = text[-4].split("–")[-1].strip()
        #     family = text[-3].split("–")[-1].strip()
        # if self.contains_cyrillic(squad):
        #     squad = ""
        #     family = ""

        return lat_name, ru_name, img, squad, family

    def _get_classification_info(self, soup: bs4.BeautifulSoup, classification_name: str):
        elements = soup.select("article p")

        for element in elements:
            text = element.text
            if not (classification_name in text):
                continue

            text = text.replace(classification_name+'.', '', 1).replace(classification_name, '', 1).strip()
            return text

        return ""

    @staticmethod
    def print_insect(insect_dict):
        print("-"*50)
        for k, v in insect_dict.items():
            print(f"    {k}: {v}")
        print("-"*50)


if __name__ == "__main__":
    ciconParser = CiconParserClass()

    a = ciconParser.get_insects_links()

    for i in range(len(a)):
        print(f"{i+1}/{len(a)}")
        ciconParser.print_insect(ciconParser.get_insect(a[i]))
        time.sleep(1)

    r = ciconParser.get_insect("https://cicon.ru/golubyanka-oreas.html")
    print(r)


