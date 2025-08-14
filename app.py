import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("E-commerce Sales Dashboard")

file=pd.read_csv("ecommerce_sales_analysis.csv")
df=pd.DataFrame(file)

monthly_sales_cols = [f"sales_month_{i}" for i in range(1, 13)]
df["total_sales"] = df[monthly_sales_cols].sum(axis=1)


# Average monthly sales of each product
df["average_monthly_sales"] = df["total_sales"] / 12

# Top 5 products
top_products = df.nlargest(5, "total_sales")[["product_name", "category", "total_sales"]]
st.caption(" :blue[Top 5 Products across all the Categories!]")
st.table(top_products)
st.divider()

# Total sales per category 
category_sales = df.groupby("category")["total_sales"].sum().sort_values(ascending=False) 
st.caption(":blue[Total sales per category]")
st.bar_chart(category_sales)
st.divider()

# Average review score per category
# category_reviews = df.groupby("category")["review_score"].mean().sort_values(ascending=False)
# y = category_reviews
# mylabels =  category_reviews.index

# st.caption(":blue[Average Review Score by Category]")
# fig1, ax1 = plt.subplots()
# ax1.pie(y, labels=mylabels, autopct='%1.1f%%', startangle=90)
# ax1.axis('equal')  
# st.pyplot(fig1)
# st.divider()

# Unique Categories
categories = df["category"].unique()

# Filtering the data using multiselect where user can select multiple categories

selected_categories = st.multiselect("Select Category", categories, default=categories)
filtered_df = df[df["category"].isin(selected_categories)]
monthly_cols = [f"sales_month_{i}" for i in range(1,13)]
category_monthly_sales = filtered_df.groupby("category")[monthly_cols].sum().T

# Show highest rated category within the selected categories
category_score = filtered_df.groupby("category")["review_score"].mean()
highest_rated_category= category_score.idxmax()
highest_rated_category_score= category_score.max()

if st.checkbox("Show highest rated category with its avg score"):
    st.markdown(f"Highest rated category is - **'{highest_rated_category }'**")
    st.markdown(f"Category Score : **'{highest_rated_category_score :.2f}'**")
    st.divider()

# top 5 products on  the basis of categories selected
top_products_on_category = filtered_df.nlargest(5, "total_sales")[["product_name", "category", "total_sales"]]
st.caption(" :blue[Top 5 Products based on categories selected!]")
st.table(top_products_on_category)
st.divider()

# Line chart and dataframe visualization of data on multiple categories selected
st.caption(":blue[Visualization of monthly sales of all the produts belonging to specific category.]")
st.line_chart(category_monthly_sales)
st.caption(":blue[ Tabular representation of monthly sales of all the produts belonging to a specific category. ]")
st.dataframe(category_monthly_sales)

