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


# #############################################################################
def get_value_or_default(dict, key, default) -> float:
    try:
        return float(dict[key][0])
    except KeyError as ex:
        st.warning(f"No value for {key.replace('_', ' ')}, defaulting to {default}")
        return default


params = st.experimental_get_query_params()
price = get_value_or_default(params, 'price', 0.0)
size = int(get_value_or_default(params, 'size', 0))
sqm_rent = get_value_or_default(params, 'sqm_rent', .0)

st.header("Apartment")
col1, col2 = st.columns(2)
price = col1.number_input('Price (€)', format='%.d', step=5000.00, key='price', value=price)
size = col2.number_input('Size (sqm)', format='%.d', step=1, key='size', value=size)

st.header("Loan")
col1, col2, col3 = st.columns((1, 2, 1))
stake = col2.slider('Personal stake (%)', 20, 40, 20, format="%.0f%%", key="stake") / 100
personal_investment = price * stake
loan = price - personal_investment
col1.metric(label="Stake", value=f'{personal_investment :,.0f}€', delta=f"{stake / 100:.0%}")
col3.metric(label="Loan", value=f'{loan :,.0f}€', delta=f"{(1 - stake):.0%}")
st.progress(stake)

st.header("Area")
col1, col2 = st.columns(2)
sqm_rent = col1.number_input('Rent/sqm/year (€)', format='%.d', step=5000.00, key='sqm_rent', value=sqm_rent)
sqm_rent_peak = col2.slider('Peak month amplifier (%)', 50, 100, 100, format="%.0f%%") / 100
peak_start = col1.date_input('Peak start', key='peak_start').month
peak_end = col2.date_input('Peak end', key='peak_end').month
peak_months = peak_end - peak_start + 1
off_peak_months = 12 - peak_months

st.header("Rent")
col1, col2, col3, col4 = st.columns(4)
monthly_rent = size * sqm_rent / 12
peak_monthly_rent = monthly_rent + (monthly_rent * sqm_rent_peak)

one_years_rent = off_peak_months * monthly_rent + peak_months * peak_monthly_rent

col1.metric(label="Off-peak", value=f'{monthly_rent:.0f}€', delta=f"{off_peak_months} months")
col2.metric(label="On-peak", value=f'{peak_monthly_rent:.0f}€', delta=f"{peak_months} months")
col3.metric(label="One year", value=f'{one_years_rent:,.0f}€')

months = [month for month in range(1, 13)]
rents = [[peak_monthly_rent if peak_start <= month <= peak_end else monthly_rent for month in months]]
year_in_rent = pd.DataFrame(rents, columns=months)
st.bar_chart(year_in_rent.transpose())

st.header("Down-payment")
down_payment_perc = st.slider('Yearly down-payment', 50, 100, 80, format="%.0f%%", step=5) / 100
repaid_perc = st.slider('Loan repaid', 0, 100, 100, format="%.0f%%", step=5) / 100

down_payment = one_years_rent * down_payment_perc
years_to_repaid_perc = int(loan * repaid_perc / down_payment)
remaining_loan = loan - repaid_perc * loan

col1, col2, col3 = st.columns((1, 1, 2))

col1.metric(label="Down-payment", value=f'{down_payment :,.0f}€', delta=f"-{down_payment / loan:.0%}")
col2.metric(label=f"Years to {repaid_perc:.0%} repaid", value=f'{years_to_repaid_perc :.0f} years')
col3.metric(label=f"Remaining loan", value=f'{remaining_loan :,.0f}€')

st.header("Sale")
# st.write(f"After paying {repaid_perc:}")
st.write(f"After {years_to_repaid_perc} years you will have paid {repaid_perc:.0%} of the loan, you can sell the property for {(1 - repaid_perc) * price:,.0f} to break even.")
sale_perc = st.slider('Sold for', 0, 150, 100, format="%.0f%%", step=5) / 100
st.write(f"Sold for {sale_perc * price:,.0f}€")
profit = (sale_perc * price) - remaining_loan
personal_profit = profit - personal_investment


col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Loan", value=f'{-remaining_loan:,.0f}€', delta=f"{-remaining_loan / profit if profit != 0 else 0:.0%}")
col2.metric(label="Profit", value=f'{profit:,.0f}€', delta=f"after remaining loan")
col3.metric(label="Investment", value=f'{-personal_investment:,.0f}€', delta=f"{-personal_investment / profit if profit != 0 else 0:.0%}")
col4.metric(label="Personal profit", value=f'{personal_profit:,.0f}€', delta="profit - investment")
