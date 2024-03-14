import streamlit as st
import pandas as pd
import preprocessor,helping
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df=pd.read_csv(r'D:\upes\Practice_python\streamlit\olympic\athlete_events.csv')
region_df=pd.read_csv(r'D:\upes\Practice_python\streamlit\olympic\noc_regions.csv')

df=preprocessor.preprocess(df,region_df)
st.sidebar.title("Olymics Analysis")
st.sidebar.image(r'https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg')
user_menu=st.sidebar.radio(
    'Select an option:',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete wise Analysis')
)


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helping.country_yr_lst(df)
   
    selected_yr=st.sidebar.selectbox("Select Year:",years)
    selected_country=st.sidebar.selectbox("Select Country:",country)

    medal_tally=helping.fetch_medal_tally(df,selected_yr,selected_country)
    if selected_yr=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_yr!='Overall' and selected_country=='Overall':
        st.title("Medal Overall Tally in "+str(selected_yr)+" olympics")
    if selected_yr=='Overall' and selected_country!='Overall':
        st.title(selected_country +" overall olympics performance")
    if selected_yr!='Overall' and selected_country!='Overall':
        st.title(selected_country+ " olympics performance in "+ str(selected_yr))

    st.table(medal_tally)

if user_menu=='Overall Analysis':
    st.title("Overall statistics analysis")
    yr= df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape
    sports=df['Sport'].unique().shape
    events=df['Event'].unique().shape
    atheletes=df['Name'].unique().shape
    nations=df['region'].unique().shape

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Edition")
        st.title(yr)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(atheletes)
    
    nation_yr=helping.data_yr(df,'region')
    fig = px.line(nation_yr, x="Years", y="region")
    st.header("Participating nation from 1896 to 2016")
    st.plotly_chart(fig)

    events_yr=helping.data_yr(df,'Event')
    fig = px.line(events_yr, x="Years", y="Event")
    st.header("Events over the years")
    st.plotly_chart(fig)

    atheletes_yr=helping.data_yr(df,'Name')
    fig = px.line(atheletes_yr, x="Years", y="Name")
    st.header("Atheletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),
                   robust=True,annot=True)
    plt.tight_layout()
    st.pyplot(fig)

    st.title("Most successful Atheletes")
    sport_lst=df['Sport'].unique().tolist()
    sport_lst.sort()
    sport_lst.insert(0,'Overall')

    selected_sport=st.selectbox("Select a Sport:",sport_lst)
    x=helping.medalist(df,selected_sport)
    st.table(x)

if user_menu =="Country-Wise Analysis":
    st.sidebar.title("Country-wise Analysis")
    country_lst= df['region'].dropna().unique().tolist()
    country_lst.sort()

    selected_country= st.sidebar.selectbox("Select a Country: ",country_lst)

    country_df=helping.medal_tally_yr(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.header(selected_country+ " Medal tally over the years")
    st.plotly_chart(fig)

    pt= helping.country_event_heatmap(df,selected_country)
    st.title(selected_country+" top in the following sports")
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    plt.tight_layout()
    st.pyplot(fig)

    st.title("Top 10 atheletes of "+ selected_country )
    top10_df=helping.medalist_country(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':
    athelete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athelete_df['Age'].dropna()
    x2=athelete_df[athelete_df['Medal']=='Gold']['Age'].dropna()
    x3=athelete_df[athelete_df['Medal']=='Silver']['Age'].dropna()
    x4=athelete_df[athelete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.title("Distribution of Atheletes Age ")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athelete_df[athelete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.title("Comparsion of Height Vs Weight")
    sport_lst=df['Sport'].unique().tolist()
    sport_lst.sort()
    sport_lst.insert(0,'Overall')
    selected_sport=st.selectbox("Select a Sport",sport_lst)
    temp_df=helping.wght_vs_hgt(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years in 1896 tp 2016")
    final = helping.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)