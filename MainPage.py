# criar pasta pages e colocar os arquivos da pagina dentro
# criar arquivo home
import pandas as pd
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config ( page_title= 'Página Principal', layout = 'wide') #  funcao para distribuir o grafico na pagina

def map_locals_rest (df1):
	#map
	cols = ['restaurant_name', 'average_cost_for_two', 'currency', 'cuisines', 'aggregate_rating', 'city', 'latitude', 'longitude']
	df_aux = df1.loc[:, cols]

	m = folium.Map()
	marker_cluster = MarkerCluster().add_to(m)

	for i, location_info in df_aux.iterrows():
		folium.Marker( [location_info['latitude'], location_info['longitude']], popup= folium.Popup(f'''<h6><br>{location_info['restaurant_name']}</br></h6><h6>Preço:{location_info['average_cost_for_two']} ({location_info['currency']}) para dois <br> Culinária: {location_info['cuisines']} <br> Avaliação: {location_info['aggregate_rating']} /5.0 </h6'''), tooltip= location_info['restaurant_name'], icon=folium.Icon(color='average_cost_for_two', icon='home', prefix='fa')).add_to( marker_cluster )
	folium_static(m, width=1024, height= 600 )
	
	return None

def convert_df(df1):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df1.to_csv().encode('utf-8')

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
image_path = 'logo_1.png'
#image = Image.open( 'logo_1.png' )
st.sidebar.image( image_path , width=190 )

st.sidebar.markdown( '# Fome Zero' )

st.sidebar.markdown('## Dados Tratados')

csv = convert_df(df1)
st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='fome_zero.csv',
    mime='text/csv',
)
#============================================
# Layout Streamlit
#============================================

st.markdown('# Fome Zero!')
st.markdown('## Encontre os restaurantes mais requisitados!')
st.markdown('### Temos as seguintes marcas dentro da plataforma:')

with st.container():
	col1, col2, col3, col4, col5 = st.columns( 5, gap='small')
	
	with col1:
		rest_tot = len( df1['restaurant_name'])
		col1.metric('Restaurantes cadastrados', rest_tot)
	with col2:
		country_tot = len( df1['country_name'].unique())
		col2.metric('Países cadastrados', country_tot)
	with col3:
		city_tot = len( df1['city'].unique())
		col3.metric('Cidades cadastradas', city_tot)
	with col4:
		votes_tot = df1['votes'].sum()
		col4.metric('Avaliações feitas','{:,.0f}'.format(votes_tot).replace(',', '.'))
	with col5:
		cuisines_tot = len( df1['cuisines'].unique())
		col5.metric('Tipos Culinários oferecidos', cuisines_tot)

# Filtros
st.sidebar.markdown( '# Filtros' )
country_options = st.sidebar.multiselect( 'Selecione os países que deseja filtrar as informações', ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], default=['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'] )

linhas_selecionadas = df1['country_name'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, :]

with st.container():
	map_locals_rest (df1)