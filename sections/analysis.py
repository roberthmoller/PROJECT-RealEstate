from sections.parameters import *
from visualizations.down_payment import visualize_payments


def down_payment(listing: Listing, loan: Loan, rent: Rent):
    with st.expander("Down-payment", expanded=True):
        year = st.slider("Years", 1, loan.years, 1, format="year %d")
        visualize_payments(loan, rent, year)


def profit():
    with st.expander("Profit"):
        st.write("bar")
