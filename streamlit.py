import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit as st

# Load your data (replace 'your_data.csv' with your actual file)
df_day = pd.read_csv("day.csv")

# Streamlit app
st.title("Bike Sharing Data Analysis")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Data Overview", "Total Users per Season", "Total User vs Temperature"])

if page == "Data Overview":
    st.header("Data Overview")
    st.write(df_day.head())
    st.write(df_day.describe())

    if st.checkbox("Show Data Info"):
        st.write(df_day.info())

    if st.checkbox("Show Data Sample"):
        st.write(df_day.sample(5))

elif page == "Total Users per Season":
    st.header("Total Users per Season")

    # Create the new DataFrame
    customer_df = df_day[['instant', 'cnt', 'season']].rename(columns={'instant': 'id', 'cnt': 'total_user'})

    # Group the DataFrame by 'season' and calculate the total customers for each season
    season_customer_totals = customer_df.groupby('season')['total_user'].sum()

    # Plotting the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(season_customer_totals.index, season_customer_totals.values, marker='o')
    ax.set_xlabel('Season (1=Spring, 2=Summer, 3=Autumn, 4=Winter)')
    ax.set_ylabel('Total User')
    ax.set_title('Total Users per Season')
    ax.set_xticks(season_customer_totals.index)
    ax.set_xticks([1, 2, 3, 4])  # Set x-axis ticks to 1, 2, 3, 4
    ax.grid(True)
    plt.yticks(season_customer_totals.values, season_customer_totals.values)
    st.pyplot(fig)

elif page == "Total User vs Temperature":
    st.header("Total User vs Temperature")
    # making line chart with first line with total_user and another line with temperature

    line_chart = alt.Chart(df_day).mark_line().encode(
        x=alt.X('season', axis=alt.Axis(values=[1, 2, 3, 4])),
        y='sum(cnt)',
        tooltip=['season', 'sum(cnt)']
    )

    line_chart2 = alt.Chart(df_day).mark_line(color='orange').encode(
        x='season',
        y='mean(temp)',
        tooltip=['season', 'mean(temp)']
    ).properties(
        title='Total User vs. Temperature',
        width=800,  # Set the width of the chart
        height=600  # Set the height of the chart
    )

    # Combine the charts using layer
    final_chart = alt.layer(line_chart, line_chart2).resolve_scale(y='independent')

    # Display the combined chart
    st.altair_chart(final_chart)
