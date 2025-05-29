import streamlit as st

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

df=pd.read_csv('Startup_Final.csv')
df.columns=df.columns.str.strip()
df.columns=df.columns.str.replace('\n','')
#st.dataframe(df)

def load_overall_Analysis():
    st.title('Overall Analysis')
    total_amt=round(df['Amount'].sum())
    max_amt = round(df['Amount'].max())
    avg_amt = round(df['Amount'].mean())
    count_startup=round(df['Startup'].nunique())
    col1,col2,col3,col4=st.columns(4)
    with col1:
     st.metric('Total',str(total_amt)+'Cr')

    with col2:
     st.metric('Max',str(max_amt)+'Cr')

    with col3:
     st.metric('Average', str(avg_amt) + 'Cr')

    with col4:
     st.metric('No. of Startups', count_startup)

    df['Date']=pd.to_datetime(df['Date'])
    df['Year']=df['Date'].dt.year
    df['Month']=df['Date'].dt.month
    st.header('Month on Month Analysis')
    selected_option=st.selectbox('Select Type',['Total','Count'])

    if selected_option=='Total':
        temp = df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()

    else:
        temp = df.groupby(['Year', 'Month'])['Amount'].count().reset_index()


    #temp = df.groupby(['Year', 'Month'])['Amount'].sum().reset_index()
    temp['X-Axis'] = temp['Year'].astype(int).astype(str) + '-' + temp['Month'].astype(int).astype(str)


    fig, ax = plt.subplots(figsize=(18,16))
    ax.plot(temp['X-Axis'], temp['Amount'],linewidth=3)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

    for label in ax.get_xticklabels():
        label.set_rotation(90)
    plt.tight_layout()
    st.pyplot(fig)


def load_investor(investor):
    st.title(investor)



      # Recent 5 investment of investors
    recent_df=df[df['Investors'].str.contains(investor)][['Date', 'Startup', 'Subvertical', 'City', 'Round', 'Amount']].sort_values(by='Date', ascending=False) .head()
    st.dataframe(recent_df)

     # Biggest 5 investments
    col1,col2=st.columns(2)
    with col1:
     big_invest=df[df['Investors'].str.contains(investor)].groupby(['Startup'])['Amount'].sum().sort_values(ascending=False).head()
     st.subheader('Biggest investments')
     st.dataframe(big_invest,width=250,height=290)

    with col2:
     st.subheader('Biggest Investments')
     fig,ax=plt.subplots()                        # All bar graphs in ax,subplot is making rectangular graph
     ax.bar(big_invest.index,big_invest.values)
     plt.xticks(fontsize=11,rotation=90)
     plt.yticks(fontsize=10)
     st.pyplot(fig)                       # The figure made bt subplot showing through this command



    # For Investor's Subvertical(Domain) Big investment

    col1,col2=st.columns(2)
    with col1:
      invest_vert=df[df['Investors'].str.contains(investor)].groupby(['Subvertical'])['Amount'].sum().sort_values(ascending=False).head()
      fig, ax = plt.subplots(figsize=(10,10))  # All graphs in ax,subplot is making pie
      ax.pie(invest_vert.values, labels=invest_vert.index,autopct='%0.2f%%')
      #plt.xticks(fontsize=11, rotation=90)
      #plt.yticks(fontsize=10)
      st.pyplot(fig)  # The figure made bt subplot showing through this command

    with col2:
      invest_city=df[df['Investors'].str.contains(investor)].groupby(['City'])['Amount'].sum().sort_values(ascending=False).head()
      fig, ax = plt.subplots(figsize=(10,10))  # All graphs in ax,subplot is making plot
      ax.pie(invest_city.values, labels=invest_city.index,autopct='%0.2f%%')
      st.pyplot(fig)

    ## YEAR ON YEAR INVESTMENTS
    df['Date']=pd.to_datetime(df['Date'])
    df['Year']=df['Date'].dt.year
    st.subheader('Investing trend of Investors Year on Year')

    yoy=df[df['Investors'].str.contains(investor)].groupby(['Year'])['Amount'].sum().sort_values(ascending=False).head()
    fig, ax = plt.subplots()
    ax.plot(yoy.index,yoy.values,marker='o',markersize=5,color='black')   # yoy.index gives years
    plt.xticks(fontsize=11, rotation=90)
    plt.yticks(fontsize=10)
    st.pyplot(fig)


st.sidebar.title('Startup Funding Analysis')

option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investors'])

if option=='Overall Analysis':
    #st.title('Overall Analysis')
    load_overall_Analysis()
    #st.sidebar.selectbox('Overall Analysis',['a','b','c'])

elif option=='Startup':
    # Sidebar filters
    df['Startup'] = df['Startup'].str.strip()
    st.sidebar.title("Select Startup")
    #filter_type = st.sidebar.selectbox("Select One", ['Startup'])
    startup_name = st.sidebar.selectbox("Select One", df['Startup'].dropna().unique())

    # Filter and show results
    if st.sidebar.button("Find Startup Details"):    # if this works
        st.title("Startups")
        #startup_name=st.sidebar.selectbox('Select Startup',df['Startup'].unique())
        startup_data = df[df['Startup'] == startup_name]
        if not startup_data.empty:
         st.subheader(f"Startup: {startup_name}")
        else:
         st.warning("No data found for the selected startup.")

            # Display each row (could be multiple entries)
        #st.write(df.columns.tolist())
        for i,row in startup_data.iterrows():
            st.markdown(f" Date : {row['Date']}")
            st.markdown(f" Industry : {row['Industry']}")
            st.markdown(f"Subvertical: {row['Subvertical']}")
            st.markdown(f"City: {row['City']}")
            st.markdown(f"Investor: {row['Investors']}")
            st.markdown(f"Funding Round: {row['Round']}")
            st.markdown(f"Amount Raised (₹ in Cr): {row['Amount']}")
            st.markdown("---")

else:
    selected_investor=st.sidebar.selectbox('Startup', sorted(set(df['Investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:            # IF button clicks
        #st.title('Investors')
        load_investor(selected_investor)


