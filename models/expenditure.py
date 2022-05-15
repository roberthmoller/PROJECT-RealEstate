from attr import dataclass

from models.rent import Rent


@dataclass
class Expenditure:
    rent: Rent
    loan: float
    maintenance: float
    savings: float

    def __getitem__(self, item):
        return self * self.rent[item]

    def __mul__(self, other):
        return Expenditure(
            rent=self.rent,
            loan=self.loan * other,
            maintenance=self.maintenance * other,
            savings=self.savings * other,
        )
