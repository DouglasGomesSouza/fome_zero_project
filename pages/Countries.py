import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config ( page_title= 'Countries', layout = 'wide') #  funcao para distribuir o grafico na pagina

def avg_price_per_country (df1):
	df_aux = df1.loc[:, ['country_name', 'average_cost_for_two']].groupby('country_name').mean().round(2).reset_index()
	fig = px.bar( df_aux, x= 'country_name', y= 'average_cost_for_two', labels= { 'country_name': 'País', 'average_cost_for_two': 'Preço de prato para duas pessoas'}, color_discrete_sequence=px.colors.qualitative.Safe, text= 'average_cost_for_two')
	fig.update_traces(textposition='outside')
	#fig.update_yaxes(showticklabels=False)
	fig.update_layout( title={ 'text' : 'Média de preço de prato para dois por país', 'y': 0.9, 'x': 0.15 } )

	return fig

def avg_votes_per_country (df1):
	df_aux = df1.loc[:, ['country_name', 'votes']].groupby('country_name').mean().round(1).reset_index() #media de avaliaçoes por pais
	fig = px.bar ( df_aux, x= 'country_name', y= 'votes', labels= { 'country_name': 'País', 'votes': 'Qtd de avaliações'}, color_discrete_sequence=px.colors.qualitative.Safe, text='votes' )
	fig.update_traces(textposition='outside')
	#fig.update_yaxes(showticklabels=False)
	fig.update_layout( title={ 'text' : 'Média de avaliações por país', 'y': 0.9, 'x': 0.2 } )
	
	return fig

def rest_per_country (df1):
	linhas_selecionadas = df1['restaurant_name'].unique()
	df_aux = df1.loc[:, ['country_name', 'restaurant_name']].groupby(['country_name']).nunique().reset_index()
	fig = px.bar ( df_aux, x = 'country_name', y = 'restaurant_name', labels={ 'country_name': 'País', 'restaurant_name': 'Qtd de restaurantes'}, color_discrete_sequence=px.colors.qualitative.Safe, text='restaurant_name' )
	fig.update_traces(textposition='outside')
	#fig.update_yaxes(showticklabels=False)
	fig.update_layout( title={ 'text' : 'Quantidade de restaurantes registrados por país', 'y': 0.9, 'x': 0.3 } )
	
	return fig

def city_per_country (df1):
	linhas_selecionadas = df1['city'].unique()
	df_aux = df1.loc[:, ['country_name', 'city']].groupby(['country_name']).nunique().reset_index()
	fig = px.bar ( df_aux, x='country_name', y='city', labels={ 'country_name': 'País', 'city': 'Qtd de cidades'}, color_discrete_sequence=px.colors.qualitative.Safe, text='city' )
	fig.update_traces(textposition='outside')
	#fig.update_yaxes(showticklabels=False)
	fig.update_layout( title={ 'text' : 'Quantidade de cidades registradas por país', 'y': 0.9, 'x': 0.3 } )
	
	return fig

def clean_code (df1):
	#renomeando as colunas dos dados
	#função que deixa tudo minusculo e separado por _
	cols_old = df1.columns 
	snakecase = lambda x: inflection.underscore(x)
	cols_new = list( map(snakecase, cols_old))

	for i in enumerate(cols_new):

		cols_new[i[0]] = cols_new[i[0]].replace(' ','_')

	df1.columns = cols_new

	#Substituindo dados da coluna CountryCode por nome dos paises
	COUNTRIES = {

	1: "India",

	14: "Australia",

	30: "Brazil",

	37: "Canada",

	94: "Indonesia",

	148: "New Zeland",

	162: "Philippines",

	166: "Qatar",

	184: "Singapure",

	189: "South Africa",

	191: "Sri Lanka",

	208: "Turkey",

	214: "United Arab Emirates",

	215: "England",

	216: "United States of America",

	}
	df1['country_code'] = df1['country_code'].map(COUNTRIES)

	df1.rename(columns={'country_code': 'country_name'}, inplace = True)

	#Substituindo dados da coluna price range
	df1.loc[df1['price_range'] == 1 , 'price_range'] = 'cheap'

	df1.loc[df1['price_range'] == 2 , 'price_range'] = 'normal'

	df1.loc[df1['price_range'] == 3 , 'price_range'] = 'expensive'

	df1.loc[df1['price_range'] == 4 , 'price_range'] = 'gourmet'

	#Substituindo dados da coluna colors pelo nome das cores
	COLORS = {

	"3F7E00": "darkgreen",

	"5BA829": "green",

	"9ACD32": "lightgreen",

	"CDD614": "orange",

	"FFBA00": "red",

	"CBCBC8": "darkred",

	"FF7800": "darkred",

	}
	
	df1['rating_color'] = df1['rating_color'].map(COLORS)

	#Deixando apenas um elemento na coluna de cuisines
	df1.loc[:, 'cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: str(x).split(',')[0])

	return df1

def country_name(country_id):

    return COUNTRIES[country_id]

def color_name(color_code):

    return COLORS[color_code]

#============================================ Inicio da Estrutura logica do codigo ============================================

df = pd.read_csv('dataset/zomato.csv')

df1 = clean_code( df )

#============================================
# Barra lateral
#============================================

st.header ( 'Visão Países' )

image_path = 'logo_1.png'
#image = Image.open( 'logo_1.png' )
st.sidebar.image( image_path , width=190 )

st.sidebar.markdown( '# Filtros' )
country_options = st.sidebar.multiselect( 'Selecione os países que deseja filtrar as informações', ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], default=['Brazil', 'England','United States of America', 'Canada'] )

st.sidebar.markdown( """---""")
st.sidebar.markdown( '### Powered by Comunidade DS')

# st.sidebar.markdown( """---""")
# if st.button('Link Exemplo'):
#     exemplo = pd.read_csv('https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv')
#     st.markdown(get_download(exemplo, 'zomato'), unsafe_allow_html=True)

# Filtro de paises

linhas_selecionadas = df1['country_name'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]

#============================================
# Layout Streamlit
#============================================

with st.container():
	fig = city_per_country(df1)
	st.plotly_chart( fig, use_container_width = True)
	
with st.container():
	fig = rest_per_country(df1)
	st.plotly_chart( fig, use_container_width = True)
	
with st.container():
	col1, col2 = st.columns( 2 )
	
	with col1:
		fig = avg_votes_per_country (df1)
		st.plotly_chart( fig, use_container_width = True)
		
	with col2:
		fig = avg_price_per_country (df1)
		st.plotly_chart( fig, use_container_width = True)