#!/usr/bin/env python
# coding: utf-8



import streamlit as st
import pandas as pd



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import altair as alt
import seaborn as sns
import plotly
import plotly.express as px
import plotly.graph_objects as go
#plt.rcParams['figure.figsize']=17,8
import cufflinks as cf
import plotly.offline as pyo
from plotly.offline import init_notebook_mode,plot,iplot
import folium 
from folium import plugins
plt.rcParams['figure.figsize'] = 10, 12
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')
#st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Covid-19 Dashboard For India</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: green;'>The dashboard will visualize the Covid-19 Situation in India</h3>", unsafe_allow_html=True)

st.markdown('______')

#df= pd.read_csv(r'C:\Users\sayan\Desktop/covid_19_india.csv')
df= pd.read_csv(r'E:\Trim III\COVID-19/covid_19_india.csv')


df.drop(['ConfirmedIndianNational','ConfirmedForeignNational'],axis=1,inplace=True)

data1 = df[['State/UnionTerritory','Confirmed','Cured','Deaths']]   

################################       Statewise Covid Status (Deaths, Cured)       ###################################

st.markdown("<h3 style='text-align: left;'>Please Select your choice of state</h3>", unsafe_allow_html=True)

all_states = ["All States",'Andaman and Nicobar Islands', 'Andhra Pradesh',
       'Arunachal Pradesh', 'Assam', 'Bihar',
       'Cases being reassigned to states', 'Chandigarh', 'Chhattisgarh',
       'Dadra and Nagar Haveli and Daman and Diu', 'Daman & Diu', 'Delhi',
       'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
       'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh',
       'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
       'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry',
       'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
       'Telengana', 'Tripura', 'Unassigned', 'Uttar Pradesh',
       'Uttarakhand', 'West Bengal']
state_choices = st.multiselect("State/UnionTerritory",all_states)
default=["All States"]









if state_choices == default:
    data = data1
    f, ax = plt.subplots(figsize=(10,10 ))
    data.sort_values('Confirmed',ascending=False,inplace=True)
    sns.set_color_codes("pastel")
    sns.barplot(x="Confirmed", y="State/UnionTerritory", data=data,label="Deaths", color="red")
    sns.set_color_codes("muted")
    sns.barplot(x="Cured", y="State/UnionTerritory", data=data, label="Cured", color="green")
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 700000), ylabel="",xlabel="Cases")
    sns.despine(left=True, bottom=True)
    st.pyplot(f)

elif state_choices == []:
    st.write("No State Selected")


else:
    data = data1.loc[data1['State/UnionTerritory'].isin(state_choices) ]
    f, ax = plt.subplots(figsize=(10,10 ))
    data.sort_values('Confirmed',ascending=False,inplace=True)
    sns.set_color_codes("pastel")
    sns.barplot(x="Confirmed", y="State/UnionTerritory", data=data,label="Deaths", color="red")
    sns.set_color_codes("muted")
    sns.barplot(x="Cured", y="State/UnionTerritory", data=data, label="Cured", color="green")
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 700000), ylabel="",xlabel="Cases")
    sns.despine(left=True, bottom=True)
    st.pyplot(f)

st.write("#")
st.write("#")
st.markdown('______')


#############################    Daily cases     ######################################

st.markdown("<h3 style='text-align: Center;'>Coronavirus Cases in India on daily basis</h3>", unsafe_allow_html=True)

df['Date'] = pd.to_datetime(df['Date'],dayfirst = True)
df_confirmed_india=df.groupby('Date')['Confirmed'].sum().reset_index()
df_cured_india=df.groupby('Date')['Cured'].sum().reset_index()
df_death_india=df.groupby('Date')['Deaths'].sum().reset_index()

import plotly.express as px
fig = px.bar(df_confirmed_india, x="Date", y="Confirmed", barmode='group', height=400)
fig.update_layout(title_text='',plot_bgcolor='coral')
st.plotly_chart(fig)


st.write("#")

st.markdown('______')

#################################     State_wise_cases      #######################

st.markdown("<h2 style='text-align: Center;'>State wise Cases</h2>", unsafe_allow_html=True)

state_cases = df.groupby('State/UnionTerritory')['Confirmed','Deaths','Cured'].max().reset_index()
state_cases['Active'] = state_cases['Confirmed'] - (state_cases['Deaths']+ state_cases['Cured'])
state_cases["Death Rate (per 100)"] = np.round(100*state_cases["Deaths"]/state_cases["Confirmed"],2)
state_cases["Cure Rate (per 100)"] = np.round(100*state_cases["Cured"]/state_cases["Confirmed"],2)

state_wise_cases=state_cases.sort_values('Confirmed', ascending= False).fillna(0).style.background_gradient(cmap='Blues',subset=["Confirmed"])\
                        .background_gradient(cmap='Reds',subset=["Deaths"])\
                        .background_gradient(cmap='Greens',subset=["Cured"])\
                        .background_gradient(cmap='autumn',subset=["Active"])\
                        .background_gradient(cmap='Wistia',subset=["Death Rate (per 100)"])\
                        .background_gradient(cmap='gist_stern_r',subset=["Cure Rate (per 100)"])


st.table(state_wise_cases)
st.write("#")

st.markdown('______')


#####################   TREE MAP  #######################

st.markdown("<h2 style='text-align: Center;'>Treemap of states comparing total deaths</h2>", unsafe_allow_html=True)
tree1 = px.treemap(state_cases,path=["State/UnionTerritory"],values="Deaths",title="")

st.plotly_chart(tree1)

st.write("#")

st.markdown('______')

################# TOP 10 _Confirmed  ######################
st.markdown("<h3 style='text-align: Center;'>Top-10 States/Union Territory with Highest No. of Confirmed Cases</h3>", unsafe_allow_html=True)

df['Fatality-Ratio'] = df['Deaths']/df['Confirmed']

top_10=state_cases.groupby('State/UnionTerritory')['Confirmed'].sum().sort_values(ascending=False).reset_index()
trace = go.Table(
    domain=dict(x=[0, 0.52],
                y=[0, 1.0]),
    header=dict(values=["State/UnionTerritory","Confirmed Cases"],
                fill = dict(color = 'black'),
                font = dict(color = 'white', size = 14),
                align = ['center'],
               height = 30),
    cells=dict(values=[top_10['State/UnionTerritory'].head(10),top_10['Confirmed'].head(10)],
               fill = dict(color = ['goldenrod']),
               align = ['center'],height=20))

trace1 = go.Bar(x=top_10['State/UnionTerritory'].head(10),
                y=top_10['Confirmed'].head(10),
                xaxis='x1',yaxis='y1',
                marker=dict(color='orange'),opacity=0.70)
layout = dict(
    width=1000,
    height=400,
    autosize=False,
    title='',
    showlegend=False,   
    xaxis1=dict(**dict(domain=[0.58, 1], anchor='y1', showticklabels=True)),
    yaxis1=dict(**dict(domain=[0, 1.0], anchor='x1', hoverformat='.2f')),  
)
fig1 = dict(data=[trace, trace1], layout=layout)
st.plotly_chart(fig1)

st.write("#")

st.markdown('______')

########################  Top 10 Recovery #####################

st.markdown("<h3 style='text-align: Center;'>Top 10 states with maximum number of Recovery</h3>", unsafe_allow_html=True)

top_10=state_cases.groupby('State/UnionTerritory')['Cured'].sum().sort_values(ascending=False).reset_index()
trace = go.Table(
    domain=dict(x=[0, 0.52],
                y=[0, 1.0]),
    header=dict(values=["State/UnionTerritory","Cured Cases"],
                fill = dict(color = 'black'),
                font = dict(color = 'white', size = 14),
                align = ['center'],
               height = 30),
    cells=dict(values=[top_10['State/UnionTerritory'].head(10),top_10['Cured'].head(10)],
               fill = dict(color = ['limegreen']),
               align = ['center'],height=20))
trace1 = go.Bar(x=top_10['State/UnionTerritory'].head(10),
                y=top_10['Cured'].head(10),
                xaxis='x1',
                yaxis='y1',
                marker=dict(color='lime'),opacity=0.70)
layout = dict(
    width=1000,
    height=400,
    autosize=False,
    title='',
    showlegend=False,   
    xaxis1=dict(**dict(domain=[0.58, 1], anchor='y1', showticklabels=True)),
    yaxis1=dict(**dict(domain=[0, 1.0], anchor='x1', hoverformat='.2f')),  
)
fig1 = dict(data=[trace, trace1], layout=layout)
st.plotly_chart(fig1)

st.write("#")

st.markdown('______')



###################### Top 10 Deaths  ###################
st.markdown("<h3 style='text-align: Center;'>Top-10 States with Highest No. of Deaths</h3>", unsafe_allow_html=True)

top_10=state_cases.groupby('State/UnionTerritory')['Deaths'].sum().sort_values(ascending=False).reset_index()
trace = go.Table(
    domain=dict(x=[0, 0.52],
                y=[0, 1.0]),
    header=dict(values=["State/UnionTerritory","Deaths Cases"],
                fill = dict(color = 'black'),
                font = dict(color = 'white', size = 14),
                align = ['center'],
               height = 30),
    cells=dict(values=[top_10['State/UnionTerritory'].head(10),top_10['Deaths'].head(10)],
               fill = dict(color = ['indianred']),
               align = ['center'],height=20))

trace1 = go.Bar(x=top_10['State/UnionTerritory'].head(10),
                y=top_10['Deaths'].head(10),
                xaxis='x1',
                yaxis='y1',
                marker=dict(color='orangered'),opacity=0.70)
layout = dict(
    width=1000,
    height=400,
    autosize=False,
    title='',
    showlegend=False,   
    xaxis1=dict(**dict(domain=[0.58, 1], anchor='y1', showticklabels=True)),
    yaxis1=dict(**dict(domain=[0, 1.0], anchor='x1', hoverformat='.2f')),  
)
fig1 = dict(data=[trace, trace1], layout=layout)
st.plotly_chart(fig1)

st.write("#")

st.markdown('______')




#############################################################################  Vaccine ##################################################################################

#df_vaccine_statewise = pd.read_csv(r'C:\Users\sayan\Desktop/covid_vaccine_statewise.csv')
df_vaccine_statewise = pd.read_csv(r'E:\Trim III\COVID-19/covid_vaccine_statewise.csv')

########  Total vaccinated  #########

st.markdown("<h3 style='text-align: Center;'>Total Individuals Vaccinated</h3>", unsafe_allow_html=True)

mask = (df_vaccine_statewise["State"]=="India")
x3 = df_vaccine_statewise[mask]["Updated On"]

y3 = df_vaccine_statewise[mask]["Total Individuals Vaccinated"]

fig = px.line(x = x3, y = y3,color_discrete_sequence=px.colors.qualitative.Dark2,
       title="")

fig.update_xaxes(title_text="Dates")
fig.update_yaxes(title_text="Number of Persons")

st.plotly_chart(fig)

st.write("#")

st.markdown('______')

###############  Total Dose   #########

st.markdown("<h3 style='text-align: Center;'>First Dose and Second Dose Administered Comparison all over India</h3>", unsafe_allow_html=True)

y5 = df_vaccine_statewise[mask]["First Dose Administered"]
y6= df_vaccine_statewise[mask]["Second Dose Administered"]


genre = st.radio("Choose any",('First Dose', 'Second Dose', 'Both'))

if genre == 'First Dose':
    anchos = 0.5
    fig = go.Figure()
    fig.add_trace(go.Bar(x = x3, 
                     y = y5,
                     width = anchos, name = 'First Dose Administered'))

    fig.update_layout(title = "",
                  title_font_size = 20,
                  width = 900, height = 500)

    st.plotly_chart(fig)

if genre == 'Second Dose':
    anchos = 0.5
    fig = go.Figure()
    fig.add_trace(go.Bar(x = x3, 
                     y = y6,
                     width = anchos, name = 'Second Dose Administered'))

    fig.update_layout(title = "",
                  title_font_size = 20,
                  width = 900, height = 500)
    st.plotly_chart(fig)


if genre == 'Both':
    anchos = 0.5
    fig = go.Figure()
    fig.add_trace(go.Bar(x = x3, 
                     y = y5,
                     width = anchos, name = 'First Dose Administered'))

    fig.add_trace(go.Bar(x = x3, 
                     y = y6,
                     width = anchos, name = 'Second Dose Administered'))

    fig.update_layout(title = "",
                  barmode = 'overlay',title_font_size = 20,
                  width = 900, height = 500)
    st.plotly_chart(fig)


st.write("#")

st.markdown('______')

########## Gender wise  #######

st.markdown("<h3 style='text-align: Center;'>Male and Female Vaccinated ratio for Covid19</h3>", unsafe_allow_html=True)

male = df_vaccine_statewise["Male(Individuals Vaccinated)"].sum() 
female = df_vaccine_statewise["Female(Individuals Vaccinated)"].sum()  
trans = df_vaccine_statewise["Transgender(Individuals Vaccinated)"].sum()
pie_1 = px.pie(names=["Male Vaccinated","Female Vaccinated","Trans Gender"],values=[male,female,trans],title="")

st.plotly_chart(pie_1)

st.write("#")

st.markdown('______')

############  vaccine brand  #########
st.markdown("<h3 style='text-align: Center;'>Covaxin and Covishield Vaccination</h3>", unsafe_allow_html=True)

Covaxin = df_vaccine_statewise["Total Covaxin Administered"].sum() 
Covishield = df_vaccine_statewise["Total CoviShield Administered"].sum()  
pie_2 = px.pie(names=["Covaxin Administered","CoviShield Administered"],values=[Covaxin,Covishield],title="")

st.plotly_chart(pie_2)

st.write("#")

st.markdown('______')
