from typing import Tuple, Any, Type, Iterable, Iterator

from attr import dataclass


@dataclass
class Season:
    season: Tuple[int, int]
    increase: float


@dataclass
class Rent(Iterable):
    monthly: float

    @staticmethod
    def of(monthly: float, season: Season = None) -> 'Rent':
        if season:
            return SeasonalRent(monthly=monthly, season=season.season, increase=season.increase)
        return Rent(monthly=monthly)

    def is_seasonal(self) -> bool:
        return False

    def yearly(self) -> float:
        return self.monthly * 12

    def __getitem__(self, item: int) -> float:
        if 1 > item > 12:
            raise IndexError("Index must be between 0 and 12")
        return self.monthly

    def __iter__(self) -> Iterator[float]:
        for month in range(1, 13):
            yield self[month]


@dataclass
class SeasonalRent(Rent):
    monthly: float
    season: Tuple[int, int]
    increase: float
    seasonal = property(lambda self: self.monthly * self.increase)

    def is_seasonal(self) -> bool:
        return True

    def duration(self) -> int:
        season_start, season_end = self.season
        return season_end - season_start

    def yearly(self) -> float:
        with self.duration() as duration:
            return self.monthly * ((12 - duration) + (self.increase * duration))

    def __getitem__(self, item: int) -> float:
        if 1 > item > 12:
            raise IndexError("Index must be between 0 and 12")

        if self.season[0] <= item <= self.season[1]:
            return self.monthly * self.increase
        return self.monthly


