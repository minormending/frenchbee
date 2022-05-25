from typing import Iterable
from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, Session

from .models import Airport

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FrenchBeeData:
    def __init__(self) -> None:
        self.session: Session = Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "base_host=frenchbee.com; market_lang=en; site_origin=us.frenchbee.com",
        }
        self.session.proxies = {"http": "127.0.0.1:8888", "https": "127.0.0.1:8888"}
        self.session.verify = False

    def get_airports(self) -> Iterable[Airport]:
        url: str = f"https://us.frenchbee.com/en"
        resp: Response = self.session.get(url)

        soup: BeautifulSoup = BeautifulSoup(resp.text, "html.parser")
        source_list_tag: Tag = soup.find(
            "select", id="edit-visible-newsearch-flights-from"
        )
        source_tags: ResultSet = source_list_tag.find_all("option")
        for source_tag in source_tags:
            code: str = source_tag["value"]
            name: str = source_tag.getText()
            yield Airport(code, name)


if __name__ == "__main__":
    data = FrenchBeeData()
    for airport in data.get_airports():
        print(airport.__dict__)
