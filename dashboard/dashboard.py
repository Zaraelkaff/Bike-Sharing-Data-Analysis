import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Fungsi untuk menghitung total pemesanan masing-masing user
def cnt_user(df):
    casual = df['casual'].sum()
    registered = df['registered'].sum()
    count = df['count'].sum()
    return casual,registered,count

# Fungsi membuat line plot
def make_Line_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df_x,df_y)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10,rotation=labelrotation)
    st.pyplot(fig)

# Fungsi untuk menghitung total pemesanan masing-masing time category
def cnt_timecat(df):
    data = df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    if data.empty:
        Morning=0
        Afternoon=0
        Evening=0
        Night=0
    else:
        Morning = data.loc[data['time_category']=='Morning','count'].values[0]        
        Afternoon = data.loc[data['time_category']=='Afternoon','count'].values[0]
        Evening = data.loc[data['time_category']=='Evening','count'].values[0]
        Night = data.loc[data['time_category']=='Night','count'].values[0]
    return Morning, Afternoon, Evening, Night

# Fungsi membuat bar plot
def make_bar_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    figx, ax = plt.subplots(figsize=(6, 6))
    ax.bar(df_x, df_y, color='#72BCD4')
    ax.tick_params(axis='x', labelsize=10,rotation=labelrotation)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    st.pyplot(figx)

# Baca File csv
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# mengolah data
day_df.sort_values(by="rental_date", inplace=True)
hour_df.sort_values(by="rental_date", inplace=True)
day_df['rental_date'] = pd.to_datetime(day_df['rental_date'])
hour_df['rental_date'] = pd.to_datetime(hour_df['rental_date'])

# Membuat Sidebar 
min_date = hour_df["rental_date"].min()
max_date = hour_df["rental_date"].max()
with st.sidebar:
    st.image("dashboard/logo.png")

    # Membuat filter rentang tanggal
    start_date, end_date = st.date_input(
        label='time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mengolah data sesuai rentang tanggal yang diinput
main_day_df = day_df[(day_df["rental_date"] >= str(start_date)) & (day_df["rental_date"] <= str(end_date))]
main_hour_df = hour_df[(hour_df["rental_date"] >= str(start_date)) & (hour_df["rental_date"] <= str(end_date))]

# Dashboard
st.title('Welcome To Rental Bersama IMA :sparkles:')
st.markdown("""---""")

# Membuat Grafik pemesanan harian
st.header('Daily Rentals :date:')
tab1, tab2, tab3 = st.tabs(["ALL","holiday", "working day"])
# Grafik jumlah rental di semua hari (sesuai rentang yang diinput)
with tab1:
    casual,registered,count = cnt_user(main_day_df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_Line_Plot(main_day_df['rental_date'],main_day_df['count'],None,None,45) 

# Grafik jumlah rental di hari libur (sesuai rentang yang diinput)
with tab2:
    df_holiday = main_day_df[main_day_df['holiday']==1]
    casual,registered,count = cnt_user(df_holiday)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_Line_Plot(df_holiday['rental_date'],df_holiday['count'],None,None,45)

# Grafik jumlah rental di hari kerja (sesuai rentang yang diinput)
with tab3:
    df_workday = main_day_df[main_day_df['workingday']==1]
    casual,registered,count = cnt_user(df_workday)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Casual User")
        st.subheader(casual)
    with col2:
        st.write("Registered User")
        st.subheader(registered)    
    with col3:
        st.write("Count")
        st.subheader(count)
    make_Line_Plot(df_workday['rental_date'],df_workday['count'],None,None,45)

# Membuat Grafik pemesanan berdasarkan kategori waktu (Pagi, Siang, Sore, Malam)
st.markdown("""---""")
st.header('Hourly Rentals :clock1:')
tab1, tab2, tab3 = st.tabs(["ALL","holiday", "working day"])

# Grafik jumlah rental di semua hari (sesuai rentang yang diinput)
with tab1:
    st.subheader("Count User")
    col1, col2, col3 = st.columns([1,1,2])
    hourly_cnt_df = main_hour_df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    Morning, Afternoon, Evening, Night = cnt_timecat(hourly_cnt_df)
    with col1:        
        st.metric(label="Morning", value=Morning)
        st.metric(label="Afternoon", value=Afternoon)
    with col2:
        st.metric(label="Evening", value=Evening)
        st.metric(label="Night", value=Night)
    with col3:
        make_bar_Plot(hourly_cnt_df["time_category"],hourly_cnt_df["count"],None,'count',45)

# Grafik jumlah rental di hari libur (sesuai rentang yang diinput)
with tab2:
    st.subheader("Count User")
    col1, col2, col3 = st.columns([1,1,2])
    hourly_cnt_df = main_hour_df[main_hour_df['holiday']==1]
    hourly_cnt_df = hourly_cnt_df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    Morning, Afternoon, Evening, Night = cnt_timecat(hourly_cnt_df)
    with col1:        
        st.metric(label="Morning", value=Morning)
        st.metric(label="Afternoon", value=Afternoon)
    with col2:
        st.metric(label="Evening", value=Evening)
        st.metric(label="Night", value=Night)
    with col3:
        make_bar_Plot(hourly_cnt_df["time_category"],hourly_cnt_df["count"],None,'count',45)

# Grafik jumlah rental di hari kerja (sesuai rentang yang diinput)
with tab3:
    st.subheader("Count User")
    col1, col2, col3 = st.columns([1,1,2])
    hourly_cnt_df = main_hour_df[main_hour_df['workingday']==1]
    hourly_cnt_df = hourly_cnt_df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    Morning, Afternoon, Evening, Night = cnt_timecat(hourly_cnt_df)
    with col1:        
        st.metric(label="Morning", value=Morning)
        st.metric(label="Afternoon", value=Afternoon)
    with col2:
        st.metric(label="Evening", value=Evening)
        st.metric(label="Night", value=Night)
    with col3:
        make_bar_Plot(hourly_cnt_df["time_category"],hourly_cnt_df["count"],None,'count',45)

# Membuat Grafik korelasi temperature dan count rental
st.markdown("""---""")
st.header('Temperature Correlation :thermometer:')
col1,col2=st.columns([7,1])
with col1:
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.scatter(x=main_day_df['temp'],  y=main_day_df['count'])
    ax.set_ylabel('Count Rental')
    ax.set_xlabel('Temperature')
    st.pyplot(fig)
with col2:
    corr = main_day_df['temp'].corr(main_day_df['count'])
    st.metric(label="Korelasi", value=round(corr,2))
