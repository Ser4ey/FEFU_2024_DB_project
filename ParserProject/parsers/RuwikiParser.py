import re
import time

import bs4
import requests
from bs4 import BeautifulSoup

from .AbstractInsectParser import AbstractInsectParser


class RuWikiParserClass(AbstractInsectParser):
    insects_catalogue_url = "https://ru.ruwiki.ru/wiki/Список_насекомых,_занесённых_в_Красную_книгу_России"

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
        r = self._get(RuWikiParserClass.insects_catalogue_url)
        soup = BeautifulSoup(r, 'lxml')
        blocks = soup.select("table.wikitable tr")

        links = []
        for i in range(len(blocks)):
            tds = blocks[i].find_all('td')
            if len(tds) != 5:
                print("no")
                continue

            link = "https://ru.ruwiki.ru" + tds[1].find("a").get("href")
            links.append(link)

        return links

    def get_insect(self, url: str):
        r = self._get(url)
        soup = BeautifulSoup(r, 'lxml')

        squad = self._get_classification_info(soup, "Отряд:")
        if not self.is_only_ru_letters(squad):
            squad = ""
        squad = squad.capitalize()

        family = self._get_classification_info(soup, "Семейство:")
        if not self.is_only_ru_letters(family):
            family = ""
        family = family.capitalize()

        return {
            "lat_name": self._get_lat_name(soup),
            "ru_name": self._get_ru_name(soup),
            "img": self._get_img(soup),

            "squad": squad,
            "family": family,

            "description": self._get_info_block(soup, "Описание"),
            "distribution": self._get_info_block(soup, "Распространение"),
            "area": self._get_info_block(soup, "Ареал"),
            "habitat": self._get_info_block(soup, "Местообитания"),
            "limiting_factors": self._get_info_block(soup, "Лимитирующие_факторы"),
            "count_": self._get_info_block(soup, "Численность"),
            "security_notes": self._get_info_block(soup, "Замечания_по_охране"),
        }

    def _get_lat_name(self, soup: bs4.BeautifulSoup):
        pattern = "\(лат\.([^)]+)\)"
        match = re.search(pattern, soup.text)

        if match:
            latin_name = match.group(1)
            if self.contains_cyrillic(latin_name):
                return ""
            return latin_name.strip()
        else:
            return ""

    def _get_ru_name(self, soup: bs4.BeautifulSoup):
        return soup.find("span", class_="mw-page-title-main").text

    def _get_img(self, soup: bs4.BeautifulSoup):
        try:
            return soup.find("td", class_="infobox-image").find("img").get("src")
        except:
            return ""

    def _get_classification_info(self, soup: bs4.BeautifulSoup, classification_name: str):
        element = soup.find('div', class_='ts-Taxonomy-rang-label', string=classification_name)

        if element is None:
            element2 = soup.find(lambda tag: tag.name == "th" and classification_name in tag.text)
            if not (element2 is None):
                element3 = element2.find_next_sibling()
                if not (element3 is None):
                    return element3.text.strip()

        return element.find_next_sibling("div").find("a").text.strip()

    def _get_info_block(self, soup: bs4.BeautifulSoup, block_name: str):
        description = soup.find(id=block_name)
        if description is None:
            return ""

        description_text = description.parent.find_next_sibling("p")
        return description_text.text.strip()

    @staticmethod
    def print_insect(insect_dict):
        print("-"*50)
        for k, v in insect_dict.items():
            print(f"    {k}: {v}")
        print("-"*50)

    @staticmethod
    def contains_cyrillic(text):
        # Регулярное выражение для русских букв в Unicode
        cyrillic_pattern = re.compile('[\u0400-\u04FF]')
        # Проверяем, соответствует ли строка шаблону
        return bool(cyrillic_pattern.search(text))

    @staticmethod
    def is_only_ru_letters(s):
        return bool(re.fullmatch('[а-яА-ЯёЁ]+', s))


if __name__ == "__main__":
    ruWikiParser = RuWikiParserClass()

    a = ruWikiParser.get_insects_links()

    for i in range(len(a)):
        print(f"{i+1}/{len(a)}")
        ruWikiParser.print_insect(ruWikiParser.get_insect(a[i]))
        time.sleep(1)



