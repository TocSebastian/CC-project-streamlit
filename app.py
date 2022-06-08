import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.io import gbq
import requests
from PIL import Image
import pandas_gbq
from bs4 import BeautifulSoup
from google.oauth2 import service_account

img = Image.open('logo.svg.png')
st.set_page_config(page_title = 'Movies IMDb',page_icon=img, layout='wide',initial_sidebar_state='collapsed',)

st.header("Movie Dataframe")
st.header(' ')

query = "SELECT * FROM `cc-project-351909.cc_dataset.movies`"
df = pandas_gbq.read_gbq(query, project_id = 'cc-project-351909', credentials = service_account.Credentials.from_service_account_file('privatekey.json'))

df = df.astype({"year":int, "nota":float})



nota_colors = ['red', 'yellow', 'green']
nota_dict = {'red':range(0,5),'yellow':range(4,7),'green':range(6,11),'all':range(0,11)}   # dictionar pentru metascore
sort_valori = ['nota','year']  

title_sidebar = st.sidebar.header("Filtre")                                                                 # titlu Sidebar


x = st.sidebar.slider('Alege un an', int(min(df.year.unique())), int(max(df.year.unique())),(1990,2010))

metascore_container = st.sidebar.container()                                    #
all_nota = st.sidebar.checkbox("Select all nota")                          #
if all_nota:                                                                    #
    nota = 'all'                                                           #  ---> metascore sidebar widget
else:                                                                           #
    nota = st.sidebar.select_slider('Nota', nota_colors, 'green')          #
                                                                                #
color = nota_dict[nota] 

sortare = st.sidebar.multiselect('Sorteaza dupa:', sort_valori, 'nota') 

df_years = df.loc[(df.year>=x[0]) & (df.year<=x[1])&(df.nota >= min(color))  & (df.nota <=max(color))]    # aici are loc sortarea in functie de parametrii de mai sus inafara de actori si directori
df_final= df_years.sort_values(sortare, ascending = False)

def color_df(val):
        if val > 6:
            color = 'green'
        elif val > 4:
            color = 'orange'                                                    # functie pentru a colora valorile din coloana metascore in functie de valoarea lor
        elif val > 0:
            color = 'red'
        return f'background-color: {color}'
st.dataframe(df_final.style.applymap(color_df, subset = ['nota']))

df_csv = df_final.to_csv()
                                                                                # convertim dataframe-ul in csv si oferim posibilitatea de al downloada
st.download_button('Download CSV here',df_csv)


col1,col2,col3,col4 = st.columns(4)

with col1:
    x_label = st.selectbox('Ox',['year'])
with col2:
    y_label = st.selectbox('Oy',['nota'])
with col3:                                                                                   # cele 4 optiuni pentru afisarea graficelor
    function = st.selectbox('Functions',['mean','max','min'])
with col4:
    numb_years = st.selectbox('Pass',['1 year','5 years','10 years','25 years'])
    numb_years_dict = {'1 year':1,'5 years':5,'10 years':10,'25 years':25}
    df_final['year'] = df_final['year'] - df_final['year'] % numb_years_dict[numb_years]

# -----------------------------------------------------------------------------------------------


df_plot = df_final.groupby(x_label,as_index=False).agg({y_label:function})                   # dataframe-ul care urmeaza a fi afisat in funtie de valorile optiunilor de mai sus(cele 4)

# -----------------------------------------------------------------------------------------------
def barPlot():
    fig = plt.figure(figsize=(12,4))
    sns.barplot(x =x_label, y = y_label, data = df_plot)                                     # functie pentru a afisa BarPlot
    plt.xticks(rotation = 90)
    st.pyplot(fig)
# -----------------------------------------------------------------------------------------------
def linePlot():
    fig = plt.figure(figsize=(10,4))
    sns.lineplot(x =x_label, y = y_label, data = df_plot)                                    # functie pentru a afisa LinePlot
    plt.xticks(rotation = 45)
    st.pyplot(fig)
# -----------------------------------------------------------------------------------------------

def execute_graph(graph_type):
    return {'LinePlot': lambda : linePlot(),                                                 # functie care face plotul in functie de tipul de plot ales
                    'BarPlot': lambda : barPlot()
    }[graph_type]()
# -----------------------------------------------------------------------------------------------
graph_type = st.selectbox("Alege un tip de grafic",['LinePlot','BarPlot'])
graph_type                                                                                   # alegem un tip de plot si il afisam
execute_graph(graph_type)
# -----------------------------------------------------------------------------------------------
dist_type = st.selectbox('DistPlot',['year','nota','metascore'])
def distPlot():
    fig = plt.figure(figsize=(10,4))
    sns.distplot(df_final[dist_type])                                                        # afisam un Distribution Plot in functie de parametrul ales
    plt.xticks(rotation = 45)
    st.pyplot(fig)
distPlot()