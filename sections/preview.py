import streamlit as st

from util import image
from models.listing import Listing


def key_details(listing: Listing):
    global c1, c2
    st.metric('Price', f"{listing.price}{listing.currency}")
    c1, c2, c3 = st.columns(3)
    c1.metric('Size', f'{listing.size}m²')
    c2.metric('Rooms', listing.rooms)
    c3.metric('Bedrooms', listing.bedrooms)
    st.metric('Location', listing.location)


def images(listing: Listing):
    with st.expander("Images"):
        st.image([image.of(uri) for uri in listing.images], caption=listing.images, channels='BGR')
