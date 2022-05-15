from typing import List

from attr import dataclass


@dataclass
class LoanTarget:
    stake: float
    target: float

    investment = property(lambda self: self.stake * self.target)
    loan = property(lambda self: self.target - self.investment)


@dataclass
class Loan(LoanTarget):
    interest: float
    years: int

    initial_yearly_interest = property(lambda self: self.loan * self.interest)
    initial_monthly_interest = property(lambda self: self.initial_yearly_interest / 12)

    def interest_for(self, principal, days=0, years=0, months=0) -> float:
        return principal * (self.interest / 365) * (days + (years * 365) + (months * (365 / 12)))

    def reduce(self, amount):
        return Loan(self.stake, self.target - amount, self.interest, self.years)

    def after_paying(self, rent):
        return DownPayment();


@dataclass
class Payment:
    loan: float
    interest: float
    total = property(lambda self: self.loan + self.interest)


@dataclass
class DownPayment:
    loan: Loan
    payments: List[Payment] = []

    def pay(self, amount: float):
        current_interest = self.loan.loan * (self.loan.interest / 365) * (365 / 12)
        amount_for_loan = amount - current_interest
        self.loan = self.loan.reduce(amount_for_loan)
        payment = Payment(interest=current_interest, loan=amount_for_loan)
        self.payments.append(payment)
        return payment

    def paid(self):
        return Payment(
            loan=sum(payment.loan for payment in self.payments),
            interest=sum(payment.interest for payment in self.payments),
        )

    def paid_until(self, month):
        return Payment(
            loan=sum(payment.loan for payment in self.payments[:month]),
            interest=sum(payment.interest for payment in self.payments[:month]),
        )
