from babel.numbers import format_currency
from helper_func import DataAnalyzer, BrazilMapPlotter
import streamlit as st
import urllib.request
import matplotlib.image as mpimg
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
sns.set(style='dark')

# load dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("./data/all_df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

geolocation = pd.read_csv("./data/geolocation.csv")
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Site Bar
with st.sidebar:
    # Logo
    st.image("logo1.png")

    # Range date
    start_date, end_date = st.date_input(
        label='Time Period',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) &
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)
brazil_map = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()  # done
sum_orders_df = function.create_sum_orders_df()  # done
monthly_orders_df = function.create_monthly_orders_df()
sum_revenue_df = function.create_sum_revenue_df()
sum_payments_df = function.create_sum_payments_df()  # done
by_state = function.create_sum_by_state_df()  # done
rfm = function.create_rfm_df()

# Title
st.header('Gunadarmart E-Commerce Dashboard :convenience_store:')

# Daily orders
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df["order_count"].sum()
    st.metric("Total orders: ", value=total_orders)

with col2:
    total_revenue = format_currency(
        daily_orders_df["revenue"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Product performance
st.subheader("Best & Worst Performing Products")

top_products = sum_orders_df.head(5)
bottom_products = sum_orders_df.tail(5)

fig, axes = plt.subplots(ncols=2, figsize=(16, 6), sharex=False)

sns.set_style("whitegrid")

# Plot Best Performing Products
sns.barplot(
    y=top_products['product_category_name_english'],
    x=top_products['order_item_id'],
    ax=axes[0],
    palette='Blues_r',
    legend=False
)
axes[0].set_title('Best Performing Products', fontsize=18, fontweight='bold')
axes[0].set_xlabel('Number of Sales', fontsize=14)
axes[0].set_ylabel('')
axes[0].tick_params(axis='y', labelsize=14)
axes[0].tick_params(axis='x', labelsize=12)
axes[0].grid(axis='x', linestyle='--', alpha=0.7)

# Plot Worst Performing Products
sns.barplot(
    y=bottom_products['product_category_name_english'],
    x=bottom_products['order_item_id'],
    ax=axes[1],
    palette='Reds_r',
    legend=False
)
axes[1].set_title('Worst Performing Products', fontsize=18, fontweight='bold')
axes[1].set_xlabel('Number of Sales', fontsize=14)
axes[1].set_ylabel('')
axes[1].yaxis.set_label_position("right")
axes[1].yaxis.tick_right()
axes[1].tick_params(axis='y', labelsize=14)
axes[1].tick_params(axis='x', labelsize=12)
axes[1].grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig)

# Tab demografi customer
st.subheader('Customer Demographic')
tab1, tab2, tab3 = st.tabs(["State", "Payment", "Geolocation"])

with tab1:
    st.header("State")

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.barplot(
        x="customer_state",
        y="customer_count",
        hue="customer_state",
        dodge=False,
        data=by_state,
        palette="viridis",
        legend=False,
        ax=ax
    )

    ax.set_ylabel("Number of Customers", fontsize=12)
    ax.set_xlabel("State", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    st.pyplot(fig)


with tab2:
    st.header("Payment Method")

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        x=sum_payments_df['payment_type'],
        y=sum_payments_df['percentage'],
        hue=sum_payments_df['payment_type'],
        palette="Blues_d",
        ax=ax
    )

    ax.set_title("Payment Type Distribution", fontsize=18)
    ax.set_xlabel("Payment Type", fontsize=14)
    ax.set_ylabel("Persentase", fontsize=14)
    ax.legend().remove()

    for i, v in enumerate(sum_payments_df['percentage']):
        ax.text(i, v + 0.01, f'{v*100:.1f}%', ha='center', fontsize=12)

    plt.tight_layout()
    st.pyplot(fig)


with tab3:
    st.header("Geolocation")
    brazil_map.plot()

    with st.expander("See Explanation"):
        st.write('Based on the customer distribution map, the average customer lives in the southeast and south. In addition, customers are also widely distributed in cities that are capital cities, such as São Paulo, Rio de Janeiro, Porto Alegre, and others.')

# Subjudul
st.subheader("Best Customer Based on RFM Parameters")

# Buat tab
tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

# Plot untuk Recency
with tab1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(y=rfm.index[:10], x=rfm['Recency'][:10],
                hue=rfm.index[:10], palette='Blues', legend=False, ax=ax)
    ax.set_title('Top 10 Customers by Recency (days)')
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    st.pyplot(fig)

# Plot untuk Frequency
with tab2:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(y=rfm.index[:10], x=rfm['Frequency'][:10],
                hue=rfm.index[:10], palette='Greens', legend=False, ax=ax)
    ax.set_title('Top 10 Customers by Frequency')
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    st.pyplot(fig)

# Plot untuk Monetary
with tab3:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(y=rfm.index[:10], x=rfm['Monetary'][:10],
                hue=rfm.index[:10], palette='Oranges', legend=False, ax=ax)
    ax.set_title('Top 10 Customers by Monetary Value')
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xscale("log")
    st.pyplot(fig)
