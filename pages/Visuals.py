
import streamlit as st
import pandas as pd
import json
import altair as alt
import os

# PAGE CONFIGURATION
st.set_page_config(page_title="Visuals", page_icon="📈")
st.title("Data Visualizations 📈")

# PART 1: GRAPHS FROM data.json
st.header("Part 1: Cosmetic Brand Market Data")

# OPEN AND READ JSON FILE
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_file = os.path.join(project_folder, "data.json")

try:
    with open(json_file, "r") as file:
        data = json.load(file)

except:
    st.error("Could not open data.json.")
    st.stop()

# CONVERT JSON DATA TO DATAFRAME
df = pd.DataFrame(data["data_points"])

if len(df) == 0:
    st.warning("There is no data in the JSON file.")
    st.stop()

elif "label" not in df.columns or "value" not in df.columns:
    st.error("The JSON file needs label and value.")
    st.stop()

# GET BRAND NAMES AND REVENUES
brands = []
revenues = []

for i in range(len(df)):
    brand = df["label"].iloc[i]
    revenue = df["value"].iloc[i]

    brands.append(brand)
    revenues.append(revenue)


# GRAPH 1: STATIC BAR CHART
st.subheader("Graph 1: Annual Revenue by Cosmetic Brand")

st.write(
    "This graph compares the annual revenue of different cosmetic "
    "brands to identify which brands lead the market and how large "
    "the differences in revenue are."
)

st.bar_chart(df, x="label", y="value")

st.divider()


# GRAPH 2: DYNAMIC SCATTER CHART
st.subheader("Graph 2: Interactive Cosmetic Brand Revenue")

st.write("Select which cosmetic brands you would like to compare.")

# CREATE BRAND OPTIONS
brand_options = []

for brand in brands:
    if brand not in brand_options:
        brand_options.append(brand)

# SESSION STATE
if "selected_brands" not in st.session_state:
    st.session_state.selected_brands = brand_options.copy()

# USER INTERACTION
selected = st.multiselect(
    "Select cosmetic brands:",
    options=brand_options,
    key="selected_brands"
)

# FILTER DATA USING LOOPS
filtered_brands = []
filtered_revenues = []

for i in range(len(brands)):
    if brands[i] in selected:
        filtered_brands.append(brands[i])
        filtered_revenues.append(revenues[i])

# CREATE FILTERED DATAFRAME
filtered_df = pd.DataFrame({
    "label": filtered_brands,
    "value": filtered_revenues
})

# CHECK SELECTIONS
if len(filtered_df) == 0:
    st.warning("Please select at least one brand.")

elif len(filtered_df) == 1:
    st.info("You are viewing one cosmetic brand.")

else:
    st.success("You are comparing multiple cosmetic brands.")


# ADVANCED ALTAIR CHART
if len(filtered_df) > 0:

    scatter_plot = alt.Chart(filtered_df).mark_circle(
        size=200
    ).encode(
        x=alt.X("label:N", title="Cosmetic Brand"),
        y=alt.Y("value:Q", title="Annual Revenue (USD Millions)"),
        color=alt.Color("label:N", title="Brand")
    ).properties(
        title="Interactive Cosmetic Brand Revenue"
    )

    st.altair_chart(scatter_plot, use_container_width=True)


    # EXTRA CREDIT: MEAN AND MEDIAN
    st.subheader("Summary Statistics")

    # CALCULATE CURRENT VALUES
    current_mean = filtered_df["value"].mean()
    current_median = filtered_df["value"].median()

    # SESSION STATE FOR PREVIOUS VALUES
    if "old_mean" not in st.session_state:
        st.session_state.old_mean = current_mean

    if "old_median" not in st.session_state:
        st.session_state.old_median = current_median

    # CALCULATE CHANGES
    mean_change = current_mean - st.session_state.old_mean
    median_change = current_median - st.session_state.old_median

    # DISPLAY METRICS
    col1, col2 = st.columns(2)

    col1.metric(
        "Mean Revenue ($M)",
        f"${current_mean:,.2f}",
        f"{mean_change:,.2f}"
    )

    col2.metric(
        "Median Revenue ($M)",
        f"${current_median:,.2f}",
        f"{median_change:,.2f}"
    )

    # UPDATE PREVIOUS VALUES
    st.session_state.old_mean = current_mean
    st.session_state.old_median = current_median

    #PART 2-------------------------------------------------------------------------------

    st.header("Part 2: Cosmetic Brand Survey Data")
    csv_file = os.path.join(project_folder, "data.csv")
    try:
        csv_df = pd.read_csv(csv_file)
    except:
        st.error("Could not open data.csv.")
        st.stop()
    if len(csv_df) == 0:
        st.warning("There is no data in the CSV file.")
        st.stop()
    elif "Category" not in csv_df.columns or "Value" not in csv_df.columns:
        st.error("The CSV file needs Category and Value columns.")
        st.stop()
        
    # CATEG AND VALUES
    csv_brands = []
    csv_ratings = []
    for i in range(len(csv_df)):
        brand_name = str(csv_df["Category"].iloc[i])
        try:
            rating_num = float(csv_df["Value"].iloc[i])
            csv_brands.append(brand_name)
            csv_ratings.append(rating_num)
        except:
            pass

    clean_csv_df = pd.DataFrame({ "Category": csv_brands, "Value": csv_ratings })
    
    # GRAPH 3: STATIC LINE CHART
    st.subheader("Graph 3: All Survey Brand Ratings")
    st.write( "This static graph displays all cosmetic brand ratings submitted " "by users on the Survey page." )
    st.line_chart(clean_csv_df, x="Category", y="Value")
    st.divider()

    # GRAPH 4: DYNAMIC BAR CHART
    st.subheader("Graph 4: Filter Survey Ratings by Minimum Score")
    st.write("Use the slider to filter cosmetic brands by their minimum rating.")
    

    if "min_rating" not in st.session_state:
        st.session_state.min_rating = 1.0

    min_score = st.slider( "Select minimum rating:", min_value=1.0, max_value=10.0, step=1.0, key="min_rating" )

    # FILTER DATA
    filtered_csv_brands = []
    filtered_csv_ratings = []
    
    for i in range(len(csv_brands)):
        if csv_ratings[i] >= min_score:
            filtered_csv_brands.append(csv_brands[i])
            filtered_csv_ratings.append(csv_ratings[i])
            filtered_csv_df = pd.DataFrame({ "Category": filtered_csv_brands, "Value": filtered_csv_ratings })

    if len(filtered_csv_df) == 0:
        st.warning("No brands match this minimum rating.")
    else:
        st.success("Showing brands that meet your minimum rating.")
        bar_plot = alt.Chart(filtered_csv_df).mark_bar().encode(
            x=alt.X("Category:N", title="Cosmetic Brand"),
            y=alt.Y("mean(Value):Q", title="Average User Rating (1-10)"),
            color=alt.Color("Category:N", title="Brand") ).properties( title="Filtered Cosmetic Brand Survey Ratings" )

        st.altair_chart(bar_plot, use_container_width=True)

    # EXTRA CREDIT: MEAN AND MEDIAN FOR CSV
    st.subheader("Survey Summary Statistics")
    
    csv_mean = filtered_csv_df["Value"].mean()
    csv_median = filtered_csv_df["Value"].median()

    if "old_csv_mean" not in st.session_state:
        st.session_state.old_csv_mean = csv_mean

    if "old_csv_median" not in st.session_state:
        st.session_state.old_csv_median = csv_median

    csv_mean_change = csv_mean - st.session_state.old_csv_mean
    csv_median_change = csv_median - st.session_state.old_csv_median

    col3, col4 = st.columns(2)

    col3.metric( "Mean Rating", f"{csv_mean:.2f}", f"{csv_mean_change:.2f}" )
    col4.metric( "Median Rating", f"{csv_median:.2f}", f"{csv_median_change:.2f}" )

    st.session_state.old_csv_mean = csv_mean
    st.session_state.old_csv_median = csv_median
        
