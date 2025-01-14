import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

#dataset
df = pd.read_csv("https://raw.githubusercontent.com/aliastrm/bikesharing_dataset/main/bikeshare-cleaned.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Bike-sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df


def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

# komponen untuk filter
min_date = df["dteday"].min()
max_date = df["dteday"].max()

# sidebar
with st.sidebar:
    st.sidebar.header("Filter:")

    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# menghubungkan filter dengan main_df
main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)

# mainpage
st.title(":bar_chart: Bike-Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# chart
fig = px.line(monthly_users_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Jumlah Bulanan Perjalanan Bikeshare").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)


fig = px.line(hourly_users_df,
              x='hr',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=["skyblue", "orange"],
              markers=True,
              title='Jumlah Perjalanan Bikeshare berdasarkan Jam Harian').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)


fig = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Jumlah Perjanan Bikeshare berdasarkan Hari Kerja dan Hari libur').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)


# left_column, right_column = st.columns(2)

# right_column.plotly_chart(fig2, use_container_width=True)

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)