import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard UTS Visualisasi Data - Netflix", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('dataset/cleaned_netflix_titles.csv')
    return df

df = load_data()

st.sidebar.header("🎛️ Filter Interaktif Dashboard")
selected_type = st.sidebar.selectbox("Pilih Tipe Konten:", options=["Semua"] + list(df['type'].unique()))

min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
selected_year_range = st.sidebar.slider("Rentang Tahun Rilis:", min_value=min_year, max_value=max_year, value=(2010, max_year))

filtered_df = df.copy()
if selected_type != "Semua":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]

filtered_df = filtered_df[
    (filtered_df['release_year'] >= selected_year_range[0]) & 
    (filtered_df['release_year'] <= selected_year_range[1])
]

st.title("📊 Dashboard Analisis Katalog Netflix")
st.markdown("**Mata Kuliah:** Visualisasi Data | **Dosen:** Muryan Awaludin, S.Kom., M.Kom.")
st.markdown("---")

st.subheader("📌 Ringkasan Utama (KPI)")
col1, col2, col3 = st.columns(3)
total_titles = len(filtered_df)
total_movies = len(filtered_df[filtered_df['type'] == 'Movie'])
total_tvshows = len(filtered_df[filtered_df['type'] == 'TV Show'])

col1.metric(label="🎬 Total Konten", value=f"{total_titles:,}")
col2.metric(label="🎥 Total Film (Movies)", value=f"{total_movies:,}")
col3.metric(label="📺 Total Serial (TV Shows)", value=f"{total_tvshows:,}")

st.markdown("---")

st.subheader("📈 Visualisasi & Eksplorasi Data")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("##### 1. Tren Pertumbuhan Konten Berdasarkan Tahun Rilis")
    trend_df = filtered_df.groupby(['release_year', 'type']).size().reset_index(name='count')
    fig_line = px.line(trend_df, x='release_year', y='count', color='type', markers=True, template='plotly_white')
    st.plotly_chart(fig_line, use_container_width=True)

with row1_col2:
    st.markdown("##### 2. Top 5 Genre/Kategori Konten Terpopuler")
    top_genres = filtered_df['listed_in'].str.split(', ').explode().value_counts().head(5).reset_index()
    top_genres.columns = ['Genre', 'Jumlah']
    fig_bar = px.bar(top_genres, x='Jumlah', y='Genre', orientation='h', text='Jumlah', color='Jumlah', color_continuous_scale='Reds', template='plotly_white')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("##### 3. Proporsi Rating Usia Penonton (Rating)")
    rating_count = filtered_df['rating'].value_counts().reset_index()
    rating_count.columns = ['Rating', 'Jumlah']
    fig_pie = px.pie(rating_count, names='Rating', values='Jumlah', hole=0.4, template='plotly_white')
    st.plotly_chart(fig_pie, use_container_width=True)

with row2_col2:
    st.markdown("##### 4. Top 5 Negara Produsen Konten Terbanyak")
    country_count = filtered_df['country'].replace('Unknown', pd.NA).dropna().str.split(', ').explode().value_counts().head(5).reset_index()
    country_count.columns = ['Negara', 'Jumlah']
    fig_country = px.bar(country_count, x='Negara', y='Jumlah', text='Jumlah', color='Jumlah', color_continuous_scale='Blues', template='plotly_white')
    st.plotly_chart(fig_country, use_container_width=True)

st.markdown("---")
st.subheader("💡 Analisis & Wawasan Utama (Key Insights)")
st.markdown("""> 1. **Lonjakan Produksi Konten:** Grafik tren menunjukkan peningkatan eksponensial jumlah rilisan konten Netflix mulai tahun 2015 hingga puncaknya pada rentang tahun 2018–2020.
> 2. **Dominasi Film (Movies):** Berdasarkan kartu KPI dan filter, katalog Netflix secara signifikan didominasi oleh format Film (*Movies*) dibandingkan Serial TV (*TV Shows*).
> 3. **Segmentasi Pasar:** Sebagian besar konten memiliki rating **TV-MA** dan **TV-14**, yang mengindikasikan bahwa target audiens utama Netflix adalah remaja dewasa dan penonton dewasa.
> 4. **Kontribusi Global:** Amerika Serikat dan India menduduki peringkat teratas sebagai negara produsen konten terbesar di platform Netflix.""")
