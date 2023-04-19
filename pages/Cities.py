import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config ( page_title= 'Cities', layout = 'wide') #  funcao para distribuir o grafico na pagina

def cuisines_top ( df1 ):
	df_aux = df1.loc[:, ['country_name', 'city', 'cuisines']].groupby(['country_name','city']).nunique().sort_values('cuisines', ascending=False).reset_index().iloc[0:10,0:10]
	fig = px.bar( df_aux, x= 'city', y= 'cuisines', labels={ 'city' : 'Cidade', 'cuisines': 'Qtd de tipos culinários distintos', 'country_name': 'País'}, color= 'country_name', color_discrete_sequence=px.colors.qualitative.Safe, text= 'cuisines')
	fig.update_traces(textposition='outside')
	#fig.update_yaxes(showticklabels=False)
	fig.update_layout( title={ 'text' : 'Top 10 cidades com mais tipos culinários', 'y': 0.9, 'x': 0.3 } )
	
	return fig

def top_worst_city ( df1 ):
	df_aux = df1.loc[(df1['aggregate_rating'] < 2.5) & (df1['aggregate_rating'] > 0 ), ['country_name','city', 'aggregate_rating']].groupby(['country_name','city']).mean().round(2).sort_values('aggregate_rating', ascending=False).reset_index().iloc[0:10,0:10]
	fig = px.bar( df_aux, x= 'city', y= 'aggregate_rating', labels={ 'city' : 'Cidade', 'aggregate_rating': 'Nota média','country_name': 'País'}, color= 'country_name', color_discrete_sequence=px.colors.qualitative.Safe, text= 'aggregate_rating')
	fig.update_traces(textposition='outside')
	fig.update_layout( title={ 'text' : 'Top 10 piores cidades', 'y': 0.9, 'x': 0.3 } )
	
	return fig

def top_city ( df1 ):
	df_aux = df1.loc[(df1['aggregate_rating'] > 4), ['country_name','city', 'aggregate_rating']].groupby(['country_name','city']).mean().round(2).sort_values('aggregate_rating', ascending=False).reset_index().iloc[0:10,0:10]
	fig = px.bar( df_aux, x= 'city', y= 'aggregate_rating', labels={ 'city' : 'Cidade', 'aggregate_rating': 'Nota média', 'country_name': 'País'}, color= 'country_name', color_discrete_sequence=px.colors.qualitative.Safe, text= 'aggregate_rating')
	fig.update_traces(textposition='outside')
	fig.update_layout( title={ 'text' : 'Top 10 melhores cidades', 'y': 0.9, 'x': 0.3 } )
	
	return fig

def rest_by_city( df1 ):
	df_aux = df1.loc[:, ['city', 'restaurant_id', 'country_name']].groupby(['country_name', 'city']).count().sort_values('restaurant_id', ascending=False).reset_index()
	fig = px.bar ( df_aux , x= 'city', y= 'restaurant_id', labels= { 'city': 'Cidade', 'restaurant_id': 'Qtd de restaurantes', 'country_name': 'País'}, color= 'country_name', color_discrete_sequence=px.colors.qualitative.Safe, text= 'restaurant_id')
	fig.update_traces(textposition='outside')
	#fig.update_yaxes(showticklabels=False)
	fig.update_layout( title={ 'text' : 'Quantidade de restaurantes por cidade', 'y': 0.9, 'x': 0.3 } )
	
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
	# rename cols
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

st.header ( 'Visão Cidades' )

image_path = 'logo_1.png'
#image = Image.open( 'logo_1.png' )
st.sidebar.image( image_path , width=190 )

st.sidebar.markdown( '# Filtros' )
country_options = st.sidebar.multiselect( 'Selecione os países que deseja filtrar as informações', ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], default=['Brazil', 'England','United States of America', 'Canada'] )

st.sidebar.markdown( """---""")
st.sidebar.markdown( '### Powered by Comunidade DS')

# Filtro de paises

linhas_selecionadas = df1['country_name'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]

#============================================
# Layout Streamlit
#============================================

with st.container():
	fig = rest_by_city( df1 )
	st.plotly_chart( fig, use_container_width = True)
	
with st.container():
	col1, col2 = st.columns( 2 )
	
	with col1:
		fig = top_city( df1 )
		st.plotly_chart( fig, use_container_width = True)
		
	with col2:
		fig = top_worst_city( df1 )
		st.plotly_chart( fig, use_container_width = True)
		
with st.container():
	fig = cuisines_top( df1 )
	st.plotly_chart( fig, use_container_width = True)