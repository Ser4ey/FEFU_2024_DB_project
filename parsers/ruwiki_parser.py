import time

import bs4
import requests
from bs4 import BeautifulSoup


class RuWikiParser:
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
        r = self._get(RuWikiParser.insects_catalogue_url)
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
        # print(r)
        # input(":")
        soup = BeautifulSoup(r, 'lxml')

        return {
            "description": self._get_info_block(soup, "Описание")
        }

    def _get_info_block(self, soup: bs4.BeautifulSoup, block_name: str):
        description = soup.find(id=block_name)
        if description is None:
            return ""

        description_text = description.parent.find_next_sibling("p")
        return description_text.text



if __name__ == "__main__":
    ruWikiParser = RuWikiParser()

    a = ruWikiParser.get_insects_links()

    for i in a:
        ruWikiParser.get_insect(i)


