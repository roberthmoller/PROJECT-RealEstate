import calendar
import dataclasses
from urllib.request import urlopen

import cv2
import numpy as np
import streamlit as st
from attr import dataclass

from image import image_of
from listing import GreenAcresListing, DummyListing, Listing

"""
# Real-estate investment analysis
Enter information about price, size, and rent in the area of possible property.

"""


@dataclass
class Loan:
    stake: float
    investment: float
    interest: float
    loan: float
    years: int


listing: Listing
loan: Loan

with st.sidebar:
    st.header("Inputs")
    url = st.text_input("Link to property")
    if url:
        listing = GreenAcresListing(url)

    if not url:
        listing = st.selectbox("Example property",
                               [DummyListing(185000, 29, "€", 2, 1, "Listing 1"),
                                DummyListing(225000, 35, "€", 4, 2, "Listing 2")],
                               format_func=lambda x: x.location)

    if listing:
        st.metric('Price', f"{listing.price}{listing.currency}")
    c1, c2, c3 = st.columns(3)
    c1.metric('Size', f'{listing.size}m²')
    c2.metric('Rooms', listing.rooms)
    c3.metric('Bedrooms', listing.bedrooms)
    st.metric('Location', listing.location)

    with st.expander("Loan"):
        personal_stake = st.slider("Personal stake", 20, 100, 20, format="%.0f%%") / 100
        investment = personal_stake * listing.price
        loan = listing.price - investment
        c1, c2 = st.columns(2)
        c1.metric("Investment", f'{investment:.0f}€', )
        c2.metric("Loan", f'{loan :.0f}€')

        interest = c1.slider("Interest rate", 0.01, 0.1, 0.05, format="%.2f%%")
        years = c2.slider("Years", 1, 30, 15)
        loan = Loan(stake=personal_stake, investment=investment, loan=loan, years=years, interest=interest)

    with st.expander("Rent"):
        sqm_rent = st.number_input("Rent/m^2", 0, 500, step=5, format="%.0d")
        rent = sqm_rent * listing.size / 12
        include_seasonal_rent = st.checkbox("Seasonal rent")
        if include_seasonal_rent:
            c1, c2 = st.columns(2)
        season_start, season_end = st.select_slider('Season duration',
                                                    options=(range(1, 13)),
                                                    format_func=lambda month: calendar.month_abbr[month],
                                                    value=(6, 8))
        peak_rent = st.slider("Rent increase", 100, 500, 200, format="%.0d%%") / 100
        seasonal_rent = (rent * peak_rent)
        c1, c2 = st.columns(2)
        c1.metric("Rent/month", f'{rent:.0f}€')
        if include_seasonal_rent: c2.metric("Seasonal/month", f'{seasonal_rent:.0f}€')
    with st.expander("Renovation"):
        st.write("foo")

if not listing:
    st.subheader("How to use")
elif listing:
    with st.expander("Images"):
        st.image([image_of(uri) for uri in listing.images], caption=listing.images, channels='BGR')

    st.subheader("Analysis")
    with st.expander("Down-payment"):
        st.write("bar")
    with st.expander("Profit"):
        st.write("bar")
