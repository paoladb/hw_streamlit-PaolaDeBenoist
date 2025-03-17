import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide")

# Load the Airbnb dataset
df = pd.read_csv("airbnb.csv")
st.title("Paola De Benoist")
# Sidebar for filters
st.sidebar.title("Filters")

# Filter by neighbourhood group
neighbourhood_group = st.sidebar.selectbox(
    "Select Neighbourhood Group", 
    df["neighbourhood_group"].unique()
)

# Filter by room type
room_type = st.sidebar.selectbox(
    "Select Room Type", 
    df["room_type"].unique()
)

# Filter by price range
price_range = st.sidebar.slider(
    "Select Price Range", 
    int(df["price"].min()), 
    int(df["price"].max()), 
    (int(df["price"].min()), int(df["price"].max()))
)

# Apply filters to the dataframe
filtered_df = df[
    (df["neighbourhood_group"] == neighbourhood_group) &
    (df["room_type"] == room_type) &
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1])
]

# Main content
st.title("Airbnb Analysis Dashboard")

# Organize the layout using columns
col1, col2 = st.columns(2)

# Top hosts in the selected neighbourhood group
with col1:
    st.subheader(f"Top Hosts in {neighbourhood_group}")
    df_host = filtered_df.groupby(["host_id", "host_name"]).size().reset_index()
    df_host["host"] = df_host["host_id"].astype(str) + "---" + df_host["host_name"]
    df_top_host = df_host.sort_values(by=0, ascending=False).head(10)
    fig = px.bar(df_top_host, x=0, y="host", orientation='h', hover_name="host_name")
    st.plotly_chart(fig)

# Boxplot for prices in the selected neighbourhood group
with col2:
    st.subheader(f"Price Distribution in {neighbourhood_group}")
    fig_boxplot = px.box(filtered_df[filtered_df["price"] < 600], x="neighbourhood", y="price")
    st.plotly_chart(fig_boxplot)

# Map of listings in the selected neighbourhood group
st.subheader(f"Map of Listings in {neighbourhood_group}")
st.map(filtered_df.dropna(), latitude="latitude", longitude="longitude")

# Create tabs for additional visualizations
tab1, tab2 = st.tabs(["Listing Type vs. Number of People", "Additional Graphs"])

# Tab 1: Relationship between listing type and the number of people
with tab1:
    st.subheader("Relationship between Listing Type and Number of People")
    fig_listing_vs_people = px.scatter(
        df, 
        x="room_type", 
        y="minimum_nights", 
        color="neighbourhood_group", 
        title="Listing Type vs. Minimum Nights"
    )
    st.plotly_chart(fig_listing_vs_people)

# Tab 2: Additional graphs
with tab2:
    st.subheader("Additional Graphs")

    # Graph 1: Price by listing type
    st.markdown("### Price by Listing Type")
    fig_price_by_type = px.box(df, x="room_type", y="price", title="Price Distribution by Listing Type")
    st.plotly_chart(fig_price_by_type)

    # Graph 2: Apartments with the highest number of reviews per month, broken down by neighborhood
    st.markdown("### Apartments with Highest Reviews per Month by Neighborhood")
    df_reviews = df.sort_values(by="reviews_per_month", ascending=False).head(50)
    fig_reviews_by_neighbourhood = px.bar(
        df_reviews, 
        x="neighbourhood", 
        y="reviews_per_month", 
        color="neighbourhood_group", 
        title="Top 50 Apartments by Reviews per Month"
    )
    st.plotly_chart(fig_reviews_by_neighbourhood)

    # Graph 3: Relationship between the number of reviews and the price
    st.markdown("### Relationship between Number of Reviews and Price")
    fig_reviews_vs_price = px.scatter(
        df, 
        x="number_of_reviews", 
        y="price", 
        color="neighbourhood_group", 
        title="Number of Reviews vs. Price"
    )
    st.plotly_chart(fig_reviews_vs_price)

# Simulator for price recommendation
st.sidebar.title("Price Recommendation Simulator")
simulator_neighbourhood = st.sidebar.selectbox(
    "Select Neighbourhood for Simulator", 
    df["neighbourhood"].unique()
)
simulator_room_type = st.sidebar.selectbox(
    "Select Room Type for Simulator", 
    df["room_type"].unique()
)
simulator_min_nights = st.sidebar.number_input(
    "Enter Minimum Nights", 
    min_value=1, 
    max_value=365, 
    value=1
)

# Calculate recommended price range based on user input
simulator_df = df[
    (df["neighbourhood"] == simulator_neighbourhood) &
    (df["room_type"] == simulator_room_type) &
    (df["minimum_nights"] >= simulator_min_nights)
]

if not simulator_df.empty:
    recommended_price_range = (simulator_df["price"].min(), simulator_df["price"].max())
    st.sidebar.markdown(f"### Recommended Price Range: €{recommended_price_range[0]} - €{recommended_price_range[1]}")
else:
    st.sidebar.markdown("### No data available for the selected criteria.")
