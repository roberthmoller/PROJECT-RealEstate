from typing import Optional

import streamlit as st
import sections.analysis as analysis
import sections.parameters as parameters
import sections.preview as preview
from models.expenditure import Expenditure
from models.listing import Listing
from models.loan import Loan
from models.rent import Rent

########################################################################################################################
# Page Config                                                                                                          #
########################################################################################################################
st.set_page_config(
    page_title="Real Estate Calculator",
    page_icon="🏘",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/roberthmoller/realestate/wiki',
        'Report a bug': "https://github.com/roberthmoller/realestate/issues/new",
        'About': "https://github.com/roberthmoller/realestate/"
    }
)

########################################################################################################################
# Header                                                                                                               #
########################################################################################################################
"""
# Real-estate Calculator
Enter information about price, size, and rent in the area of possible property.\n
Analyse the expected rent income for a year and potential profits for a sale. 
"""

########################################################################################################################
# Global state                                                                                                         #
########################################################################################################################
print("# Initialise global state")
listing: Optional[Listing]
rent: Optional[Rent]
expenditure: Optional[Expenditure]
loan: Optional[Loan]

########################################################################################################################
# Interface                                                                                                            #
########################################################################################################################
print("# Rendering Interface")
print("* Sidebar")

with st.sidebar:
    st.header("Parameters")
    listing = parameters.listing_parameters()

    if listing:
        preview.key_details(listing)
        rent = parameters.rent_parameters(listing)
        expenditure = parameters.expenditure_parameters(listing, rent)
        loan = parameters.loan_parameters(listing)


if not listing:
    print("* HowTo (no listing)")
    st.subheader("How to use")
elif listing:
    print("* Analysis")
    st.subheader("Preview")
    preview.images(listing)

    st.subheader("Analysis")
    analysis.down_payment(listing, loan, rent)
    # analysis.profit()
print("Finished rendering")
