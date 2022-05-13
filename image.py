from urllib.request import urlopen
import cv2
import numpy as np
import streamlit as st


@st.cache
def image_of(url):
    with urlopen(url) as resp:
        image = np.asarray(bytearray(resp.read()))
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
