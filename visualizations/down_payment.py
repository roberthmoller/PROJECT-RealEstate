import calendar
import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from models.colors import TRANSPARENT, WHITE
from models.loan import DownPayment


# noinspection SpellCheckingInspection
class Style:
    DEFAULT = 'default'
    GGPLOT = 'ggplot'
    FIVETHIRTYEIGHT = 'fivethirtyeight'


def visualize_payments(loan, rent, year):
    plt.style.use(Style.DEFAULT)
    fig, ax = plt.subplots(facecolor=TRANSPARENT)
    ax.set_facecolor(TRANSPARENT)
    thousand_separated_euros = plt.FuncFormatter(lambda x, p: format(int(x), ',') + '€')
    width = 1

    # Calculating interest and loan paid for one year
    down_payment = DownPayment(loan=loan)
    months = np.linspace(1, 12, 12, dtype=int)
    loan_payments = []
    interest_payments = []
    remaining_loan = []
    lats_remaining_loan = []
    calendar_year = map(lambda month: calendar.month_abbr[int(month)], months)
    for month in months:
        monthly_income = rent[month]
        monthly_downpayment = monthly_income * .8
        payment = down_payment.pay(monthly_downpayment)

        if len(remaining_loan) == 0:
            remaining_loan.append(loan.loan)
            lats_remaining_loan.append(loan.loan + payment.loan)
        else:
            remaining_loan.append(remaining_loan[-1] - payment.loan)
            lats_remaining_loan.append(remaining_loan[-1] + payment.loan)

        loan_payments.append(payment.loan)
        interest_payments.append(payment.interest)

    ax_remaining_loan = ax.bar(months, remaining_loan, label='Remaining Loan', color='magenta', width=width, alpha=0.2)
    ax_interest = ax.bar(months, interest_payments, bottom=lats_remaining_loan, label='Interest Paid', color='red', width=width, alpha=0.5)
    ax_loan = ax.bar(months, loan_payments, bottom=remaining_loan, label='Loan Paid', color='green', width=width, alpha=0.5)

    ax.bar_label(ax_interest, color='white', label_type='center', size=5, fmt="%.d €")
    ax.bar_label(ax_loan, color='white', label_type='center', size=5, fmt="%.d €")
    ax.bar_label(ax_remaining_loan, color='white', label_type='edge', size=5, padding=-10, fmt="%.d €")

    ax.set_ylim(auto=True, bottom=remaining_loan[-1] * .995, top=remaining_loan[0] * 1.01)
    ax.set_title(f'Year {year}', color=WHITE)
    ax.set_xticks(months, labels=calendar_year, color=WHITE)
    plt.gca().margins(x=0)
    ax.spines['left'].set_color(WHITE)
    ax.spines['bottom'].set_color(WHITE)
    ax.spines['right'].set_color(TRANSPARENT)
    ax.spines['top'].set_color(TRANSPARENT)
    ax.tick_params(axis='x', colors=WHITE)
    ax.tick_params(axis='y', colors=WHITE)
    ax.yaxis.set_major_formatter(thousand_separated_euros)
    ax.grid(color=WHITE, alpha=0.2, linestyle='-.', linewidth=.2, which='major', axis='y')
    ax.grid(color=WHITE, alpha=0.2, linestyle='-.', linewidth=.2, which='minor')
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(250))
    ax.legend()
    st.pyplot(plt, clear_figure=True)
