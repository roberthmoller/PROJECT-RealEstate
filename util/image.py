from io import BytesIO

import streamlit as st
from PIL import Image
from requests import get


@st.experimental_memo
def of(url):
    return Image.open(BytesIO(get(url).content))


class StockImage:
    MARS = 'http://cdn.sci-news.com/images/enlarge/image_2192_1e-Mars-Glaciers.jpg'
    VENUS = 'http://annesastronomynews.com/wp-content/uploads/2012/02/Venus1.jpg'
