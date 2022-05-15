import calendar
from enum import Enum
from typing import Optional

import streamlit as st

from models.expenditure import Expenditure
from models.listing import Listing, ExampleListings
from models.loan import Loan, LoanTarget
from models.rent import Rent, Season
from visualizations.expenditure import visualize_expenditure


class Sources(Enum):
    EXAMPLE = 'Example'
    LISTING = 'Listing'
    CUSTOM = 'Custom'

    @classmethod
    def values(cls):
        return list([cls.EXAMPLE, cls.LISTING, cls.CUSTOM])

    def __iter__(self):
        return list(self)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'Sources("{self.value}")'


def listing_parameters() -> Listing:
    sources = Sources.values()
    source_index = st.selectbox("Source", range(len(sources)), format_func=lambda i: sources[i].value)
    source = sources[source_index]
    if source == Sources.LISTING:
        url = st.text_input("Link to property")
        if url:
            return Listing.of(url)
        else:
            st.subheader("Supported domains")
            for domain in Listing.SUPPORTED_DOMAINS.keys():
                st.markdown(f'* [{domain.split("://")[-1]}]({domain})')
            return None
    elif source == Sources.EXAMPLE:
        examples = ExampleListings.all()
        example_index = st.selectbox("Example property", range(len(examples)), format_func=lambda index: examples[index].location)
        return examples[example_index]
    elif source == Sources.CUSTOM:
        raise NotImplementedError()


def rent_parameters(listing: Listing) -> Rent:
    with st.expander("Rent", expanded=True):
        sqm_rent = st.number_input("Yearly rent per m²", 0, 5000, 250, step=5, format="%.0d")
        monthly_rent = sqm_rent * listing.size / 12
        is_seasonal_apartment = st.checkbox("Seasonal rent")
        season: Optional[Season] = None
        if is_seasonal_apartment:
            season_start, season_end = st.select_slider('Season duration',
                                                        options=(range(1, 13)),
                                                        format_func=lambda month: calendar.month_abbr[month],
                                                        value=(6, 8))
            season_multiplier = st.slider("Rent increase", 100, 500, 200, format="%.0d%%") / 100
            season = Season((season_start, season_end), season_multiplier)

        rent = Rent.of(monthly=monthly_rent, season=season)
        c1, c2 = st.columns(2)
        c1.metric("Rent/month", f'{rent.monthly:.0f}€')
        c1.latex(r'r=r_{m^2}*m^2\over 12')
        if rent.is_seasonal():
            c2.metric("Seasonal/month", f'{rent.seasonal:.0f}€')
            c2.latex(r'r_s = r*s')
        return rent


def loan_parameters(listing: Listing) -> Loan:
    with st.expander("Loan", expanded=True):
        stake = st.slider("Personal stake", 20, 100, 20, format="%.0f%%") / 100
        target = LoanTarget(stake=stake, target=listing.price)

        c1, c2 = st.columns(2)
        c1.metric("Investment", f'{target.investment:.0f}€', )
        c2.metric("Loan", f'{target.loan :.0f}€')

        interest = c1.slider("Interest rate", 1.0, 4.0, 1.9, format="%.2f%%") / 100
        years = c2.slider("Years", 1, 30, 15)

        loan = Loan(stake=stake, target=listing.price, interest=interest, years=years)

        c1.metric("Monthly interest*", f'{loan.initial_monthly_interest:,.0f}€')
        c2.metric("Yearly interest*", f'{loan.initial_yearly_interest:,.0f}€')
        c1.caption(r"\*First year")

        return loan


def expenditure_parameters(listing: Listing, rent: Rent) -> Expenditure:
    with st.expander("Expenditure", expanded=True):
        st.caption("How one months rent is spent")
        loan_payment = st.slider('Loan', 0, 100, 80, format="%.0f%%") / 100
        remaining_after_loan = int((1 - loan_payment) * 100)
        if remaining_after_loan > 0:
            maintenance_payment = st.slider('Maintenance', 0, remaining_after_loan, remaining_after_loan, format="%.0f%%") / 100
        else:
            maintenance_payment = 0
        remaining_after_maintenance = int((1 - loan_payment - maintenance_payment) * 100)
        if remaining_after_maintenance > 0:
            savings_payment = st.slider('Savings', 0, remaining_after_maintenance, remaining_after_maintenance, format="%.0f%%", disabled=True) / 100
        else:
            savings_payment = 0

        visualize_expenditure(loan_payment, maintenance_payment, savings_payment)

        return Expenditure(rent=rent, loan=loan_payment, maintenance=maintenance_payment, savings=savings_payment)
