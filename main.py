import streamlit as st
import pandas as pd
import numpy as np

'''
# Real-estate investment analysis
Enter information about price, size, and rent in the area of possible property.
Calculates the expected rent income for a year.
'''

# Inputs:
# * in cost of appartment
# * egenandel
# * square meters
# * estimated price/m^2

# * number of rooms

# Transforms:
# * peak price %
# * peak time
# * income % for renovations

# Outputs:
# * suggested rent
# * suggested peak rent
# * income per year


st.header("Apartment")
col1, col2 = st.columns(2)
price = col1.number_input('Price (€)', format='%.d', step=5000.00)
size = col2.number_input('Size (sqm)', format='%.d', step=1)

st.header("Loan")
col1, col2, col3 = st.columns((1, 2, 1))
stake = col2.slider('Personal stake (%)', 20, 40, 20, format="%.0f") / 100
personal_investment = price * stake
col1.metric(label="Stake", value=f'{personal_investment :,.0f}€', delta=f"{stake / 100:.0%}")
col3.metric(label="Loan", value=f'{price - personal_investment :,.0f}€', delta=f"{(1 - stake):.0%}")

st.header("Area")
col1, col2 = st.columns(2)
sqm_rent = col1.number_input('Rent/sqm/year (€)', format='%.d', step=5000.00)
sqm_rent_peak = col2.slider('Peak month amplifier (%)', 50, 100, 100, format="%.0f") / 100
peak_start = col1.date_input('Peak start').month
peak_end = col2.date_input('Peak end').month
peak_months = peak_end - peak_start + 1
off_peak_months = 12 - peak_months



st.header("Rent")
col1, col2, col3, col4 = st.columns(4)
monthly_rent = size * sqm_rent / 12
peak_monthly_rent = monthly_rent + (monthly_rent * sqm_rent_peak)

one_years_rent = off_peak_months * monthly_rent + peak_months * peak_monthly_rent

col1.metric(label="Off-peak", value=f'{monthly_rent:.0f}€', delta=f"{off_peak_months} months")
col2.metric(label="On-peak", value=f'{peak_monthly_rent:.0f}€', delta=f"{peak_months} months")
col3.metric(label="One year", value=f'{one_years_rent:,.0f}€', delta=f"{size}")
col4.metric(label="Down-payment", value=f'{one_years_rent*.8:,.0f}€', delta=f"-80%")

months = [month for month in range(1, 13)]
rents = [[peak_monthly_rent if peak_start <= month <= peak_end else monthly_rent for month in months]]
year_in_rent = pd.DataFrame(rents, columns=months)
st.bar_chart(year_in_rent.transpose())
