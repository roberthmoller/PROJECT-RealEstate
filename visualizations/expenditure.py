import streamlit as st

from matplotlib import pyplot as plt

from models.colors import TRANSPARENT, ColorScheme


def visualize_expenditure(loan_payment, maintenance_payment, savings_payment):
    fig = plt.figure(facecolor=TRANSPARENT, figsize=(20, 20))
    ax = fig.add_axes([0, 0, 1, 1])
    labels, values = zip(*[(label, value)
                           for label, value in [
                               ('Loan', loan_payment),
                               ('Maintenance', maintenance_payment),
                               ('Savings', savings_payment)
                           ] if value > 0])
    colors = [ColorScheme.LOAN, ColorScheme.MAINTENANCE, ColorScheme.SAVINGS]
    textprops = {"fontsize": 100, "color": "white"}
    ax.pie(values, autopct='%.0f%%', explode=[0.1 for _ in labels], textprops=textprops, colors=colors)
    plt.legend(labels=labels, fontsize=100, loc='upper center', labelcolor='white', bbox_to_anchor=(0.5, -0.04), ncol=2, frameon=False)
    st.pyplot(fig)
