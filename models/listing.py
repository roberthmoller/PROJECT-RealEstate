import re
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup

from util.image import StockImage


class Listing:
    price: float = None
    currency: str = None
    size: int = None
    rooms: int = None
    bedrooms: int = None
    location: str = None
    images: List[str] = []

    SUPPORTED_DOMAINS = {}

    @staticmethod
    def get_doc(url):
        return BeautifulSoup(requests.get(url).content, "html.parser")

    def __init__(self, url: str, eager=True) -> None:
        super().__init__()
        self.url = url
        if eager:
            self.doc = self.get_doc(url)

    @classmethod
    def of(self, url: str):
        for domain, constructor in self.SUPPORTED_DOMAINS.items():
            if re.match(domain, url):
                return constructor(url)
        raise NotImplementedError()

    # Dynamically add supported domains when subclassing
    @classmethod
    def add_supported_domain(self, domain, cls):
        self.SUPPORTED_DOMAINS[domain] = cls

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__()
        if not kwargs['excluded'] if 'excluded' in kwargs else True:
            cls.add_supported_domain(kwargs['domain'], cls)


class GreenAcresListing(Listing, domain="https://www.green-acres.fr"):
    def __init__(self, url: str):
        super().__init__(url)
        details = self.doc.find_all("li", {"class": "details-component"})
        for detail in details:
            key_values = detail.text.split()
            key = ' '.join(key_values[:-1]).strip()
            value = key_values[-1].strip()

            if key.startswith("Living area"):
                self.size = int(value)
            if key.startswith("Rooms"):
                self.rooms = int(value)
            if key.startswith("Bedrooms"):
                self.bedrooms = int(value)
            if len(key_values) == 1:
                self.location = value

        self.price = float(self.doc.find("span", {"class": "price"}).text.replace(",", ""))
        self.currency = self.doc.find("span", {"class": "currency-left"}).text

        self.scripts = self.doc.find_all("script")

        image_script = [script for script in self.scripts if 'bigPhotos' in script.text][0].text
        self.images = re.findall('https://[0-9a-zA-Z.-]*[/0-9a-zA-Z-._]+/Photos[/0-9a-zA-Z-._]+', image_script)


class ExampleListing(Listing, excluded=True):
    def __init__(self, price, size, currency, rooms, bedrooms, location, images=[]) -> None:
        super().__init__("dummy listing", eager=False)
        self.location = location
        self.bedrooms = bedrooms
        self.rooms = rooms
        self.price = price
        self.currency = currency
        self.size = size
        self.images = images

    def __repr__(self) -> str:
        return f'ExampleListing(price={self.price}, size={self.size}, currency="{self.currency}", rooms={self.rooms}, bedrooms={self.bedrooms}, location="{self.location}", images={self.images})'


class ExampleListings:
    MARS = ExampleListing(185000, 29, "€", 2, 1, "Mars", [StockImage.MARS])
    VENUS = ExampleListing(225000, 35, "€", 4, 2, "Venus", [StockImage.VENUS])

    @classmethod
    def all(cls):
        return list([cls.MARS, cls.VENUS])



