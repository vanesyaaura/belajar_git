# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Dashboard Visualisasi Data")

# Memuat data
@st.cache
def load_data():
    # Contoh data sederhana
    data = {
        'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
        'Penjualan': [150, 200, 250, 300, 350, 400]
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# Menampilkan data
st.write("Data Penjualan:", df)

# Membuat grafik
fig, ax = plt.subplots()
ax.plot(df['Bulan'], df['Penjualan'], marker='o')
ax.set_xlabel('Bulan')
ax.set_ylabel('Penjualan')
ax.set_title('Penjualan per Bulan')

st.pyplot(fig)
