import re

import requests
from bs4 import BeautifulSoup


class Listing:
    def __init__(self, url: str, eager=True) -> None:
        super().__init__()
        self.url = url
        if eager:
            self.doc = self._get_listing(url)
        self.price = None
        self.currency = None
        self.size = None
        self.rooms = None
        self.bedrooms = None
        self.images = []

    def _get_listing(self, url):
        return BeautifulSoup(requests.get(url).content, "html.parser")

    @classmethod
    def of(self, url: str):
        if url.startswith("https://www.green-acres"):
            return GreenAcresListing(url)
        raise NotImplementedError()


class GreenAcresListing(Listing):
    def __init__(self, url: str):
        super().__init__(url)
        details = self.doc.find_all("li", {"class": "details-component"})
        for detail in details:
            key_values = detail.text.split()
            key = ' '.join(key_values[:-1]).strip()
            value = key_values[-1].strip()

            if key.startswith("Living area"):
                self.size = value
            if key.startswith("Rooms"):
                self.rooms = value
            if key.startswith("Bedrooms"):
                self.bedrooms = value
            if len(key_values) == 1:
                self.location = value

        self.price = self.doc.find("span", {"class": "price"}).text
        self.currency = self.doc.find("span", {"class": "currency-left"}).text

        self.scripts = self.doc.find_all("script")
        # photos
        image_script = [script for script in self.scripts if 'bigPhotos' in script.text][0].text
        self.images = re.findall('https://[0-9a-zA-Z.-]*[/0-9a-zA-Z-._]+', image_script)


class DummyListing(Listing):
    def __init__(self, price, size, currency, rooms, bedrooms, location) -> None:
        super().__init__("dummy listing", eager=False)
        self.location = location
        self.bedrooms = bedrooms
        self.rooms = rooms
        self.price = price
        self.currency = currency
        self.size = size
