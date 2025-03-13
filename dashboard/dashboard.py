import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/all_data.csv')
    return data

data = load_data()

# Judul Utama
st.title('Bike Rental Dashboard')

# Sidebar untuk filter data
st.sidebar.header('Filter Data')

# Keterangan Musim
season_mapping = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}

data['season_day'] = data['season_day'].map(season_mapping)

# Keterangan Cuaca
weather_mapping = {
    1: 'Cerah',
    2: 'Mendung',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat'
}

data['weathersit_day'] = data['weathersit_day'].map(weather_mapping)

selected_season = st.sidebar.selectbox('Pilih Musim', data['season_day'].unique())
selected_weather = st.sidebar.selectbox('Pilih Cuaca', data['weathersit_day'].unique())

# Filter data berdasarkan pilihan
filtered_data = data[(data['season_day'] == selected_season) & (data['weathersit_day'] == selected_weather)]

# Tampilkan data yang telah difilter
st.write('## Data yang Difilter')
st.write(filtered_data)

# Visualisasi 1: Distribusi Penyewaan Sepeda per Jam
st.header('Distribusi Penyewaan Sepeda per Jam')
fig, ax = plt.subplots()
sns.histplot(filtered_data['cnt_hour'], bins=30, kde=True, ax=ax)
ax.set_xlabel('Jumlah Penyewaan per Jam')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Visualisasi 2: Rata-rata Penyewaan Sepeda per Hari
st.header('Rata-rata Penyewaan Sepeda per Hari')
daily_avg = filtered_data.groupby('dteday')['cnt_day'].mean().reset_index()
fig, ax = plt.subplots()
sns.lineplot(x='dteday', y='cnt_day', data=daily_avg, ax=ax)
ax.set_xlabel('Tanggal')
ax.set_ylabel('Rata-rata Penyewaan per Hari')
plt.xticks(rotation=45, fontsize = 3)  # Rotasi sumbu x agar lebih terbaca
st.pyplot(fig)

# Visualisasi 3: Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari
st.header('Pola Penyewaan Sepeda Berdasarkan Waktu dalam Sehari')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=data, x='hr', y='cnt_hour', hue='workingday_day', palette=['red', 'blue'], ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
ax.legend(['Hari Libur', 'Hari Kerja'])
st.pyplot(fig)

# Insight Pola Penyewaan
st.write("### Insight Pola Penyewaan")
st.write("- Pada hari kerja, penyewaan sepeda meningkat tajam pada jam 7-9 pagi dan 17-19 malam.")
st.write("- Pada akhir pekan, pola penyewaan lebih stabil sepanjang hari dengan puncak pada siang dan sore hari.")
st.write("- Jam malam (setelah jam 21.00) cenderung memiliki jumlah penyewaan yang lebih rendah.")

# Visualisasi 4: Korelasi Faktor yang Mempengaruhi Penyewaan Sepeda
st.header('Korelasi antara Faktor Penyewaan Sepeda')
numeric_data = data.select_dtypes(include=['number'])
corr_matrix = numeric_data.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Insight Korelasi
st.write("### Insight Korelasi")
st.write("- Faktor yang paling berpengaruh terhadap jumlah penyewaan adalah suhu (temp, atemp) dan waktu (hr).")
st.write("- Hari kerja (workingday) dan musim (season) juga berpengaruh terhadap jumlah penyewaan.")
st.write("- Kelembaban (humidity) dan kecepatan angin (windspeed) memiliki korelasi negatif dengan jumlah penyewaan.")

# Kesimpulan Bisnis
st.header('Kesimpulan Bisnis')
st.write("- Optimalisasi jumlah sepeda pada jam sibuk dapat meningkatkan kepuasan pengguna.")
st.write("- Penyesuaian harga atau promosi pada waktu sepi dapat meningkatkan penyewaan.")
st.write("- Mempertimbangkan kondisi cuaca dalam strategi operasional bisa meningkatkan efisiensi layanan.")