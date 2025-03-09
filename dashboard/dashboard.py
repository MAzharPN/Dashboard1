import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("dashboard/all_data.csv")

df = load_data()

# Sidebar
st.sidebar.title("Dashboard Penyewaan Sepeda")
option = st.sidebar.selectbox("Pilih Visualisasi", ["Distribusi Penyewaan Harian", "Faktor Penyewaan", "Pola Penyewaan per Jam"])

# Main Title
st.title("Analisis Penyewaan Sepeda")

# Distribusi Penyewaan Harian
if option == "Distribusi Penyewaan Harian":
    st.subheader("Distribusi Penyewaan Sepeda Harian")
    fig, ax = plt.subplots()
    sns.histplot(df['cnt'], bins=50, kde=True, ax=ax)
    ax.set_xlabel("Jumlah Penyewaan")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

# Faktor Penyewaan Sepeda
elif option == "Faktor Penyewaan":
    st.subheader("Faktor yang Mempengaruhi Penyewaan Sepeda")
    selected_factors = ["temp", "hum", "windspeed", "cnt"]
    fig = sns.pairplot(df[selected_factors])
    st.pyplot(fig)

# Pola Penyewaan per Jam
elif option == "Pola Penyewaan per Jam":
    st.subheader("Rata-rata Penyewaan Sepeda per Jam")
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='hr', y='cnt', estimator='mean', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

st.write("\n**Kesimpulan:**")
st.markdown("1. Temperatur memiliki dampak besar pada jumlah penyewaan sepeda.")
st.markdown("2. Pola penyewaan menunjukkan tren commuting dengan puncak pagi dan sore hari.")
st.markdown("3. Kelembapan dan kecepatan angin tidak terlalu berpengaruh.")