import requests
from bs4 import BeautifulSoup


class RuWikiParser:
    insects_catalogue_url = "https://ru.ruwiki.ru/wiki/Список_насекомых,_занесённых_в_Красную_книгу_России"
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        }

    def get_insects_links(self):
        print(1)
        r = self.session.get(RuWikiParser.insects_catalogue_url)
        print(2)


        if r.status_code != 200:
            print(f"Error. Status code: {r.status_code} Text: {r.text}")
            exit()

        soup = BeautifulSoup(r.text, 'lxml')
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


if __name__ == "__main__":
    ruWikiParser = RuWikiParser()

    a = ruWikiParser.get_insects_links()

    print(len(a))
    print(a)

