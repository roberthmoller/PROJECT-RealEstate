from urllib.request import urlopen
import cv2
import numpy as np
import streamlit as st


@st.cache
def of(url):
    with urlopen(url) as resp:
        image = np.asarray(bytearray(resp.read()))
        return cv2.imdecode(image, cv2.IMREAD_COLOR)


class StockImage:
    MARS = r'http://cdn.sci-news.com/images/enlarge/image_2192_1e-Mars-Glaciers.jpg'
    VENUS = r'http://annesastronomynews.com/wp-content/uploads/2012/02/Venus1.jpg'
