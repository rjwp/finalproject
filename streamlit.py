# prompt: make the plot above for streamlit

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
    st.subheader("Data Analisis menggunakan fungsi describe()")
    st.write(df_day.describe())


elif page == "Total Users per Season":

    st.subheader("Line chart untuk menunjukan jumlah pengguna yang dibagi tiap season")


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

    st.write(
        "Pada line chart di atas dapat dilihat bahwa penggunaan bike sharing paling rendah ada pada musim spring dan paling tinggi pada musim autumn")

elif page == "Total User vs Temperature":
    st.subheader("Total User vs Temperature")
    # making line chart with first line with total_user and another line with temperature

    line_chart = alt.Chart(df_day).mark_line().encode(
        x=alt.X('season', axis=alt.Axis(values=[1, 2, 3, 4])),
        y=alt.Y('sum(cnt)', axis=alt.Axis(title='Total Users')),
        tooltip=['season', 'sum(cnt)']
    )

    line_chart2 = alt.Chart(df_day).mark_line(color='orange').encode(
        x='season',
        y=alt.Y('mean(temp)', axis=alt.Axis(title='mean of temperature')),
        tooltip=['season', 'mean(temp)']
    ).properties(
        title='',
        width=800,  # Set the width of the chart
        height=600  # Set the height of the chart
    )

    # Combine the charts using layer
    final_chart = alt.layer(line_chart, line_chart2).resolve_scale(y='independent')

    # Display the combined chart
    st.altair_chart(final_chart)

    st.write("Pada line chart diatas dapat dilihat terdapat korelasi positif pada data temperature dan total pengguna, "
             "yang mana semakin tinggi suhu pada saat itu maka penggunaan bike sharing cenderung meningkat dan begitu juga sebaliknya.")
