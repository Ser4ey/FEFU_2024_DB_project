from abc import ABC, abstractmethod


# Абстрактный базовый класс
class AbstractInsectParser(ABC):
    @abstractmethod
    def get_insects_links(self) -> list:
        return []

    def get_insect(self, url: str) -> dict:
        return {
            "lat_name": "",
            "ru_name": "",

            "squad": "",
            "family": "",

            "description": "",
        }
