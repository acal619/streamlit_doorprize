import streamlit as st
import random
import time
import pandas as pd

# CSS untuk gaya form dan kotak individual
st.markdown("""
    <style>
    .form-container {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    .number-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }

    .random-box {
        font-size: 48px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #3333FF;  /* Warna kotak */
        padding: 20px;
        border-radius: 10px;
        width: 70px;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        animation: bounce 0.3s infinite alternate;
    }

    .chosen-box {
        font-size: 64px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #28A745;  /* Warna kotak untuk angka terpilih */
        padding: 20px;
        border-radius: 10px;
        width: 70px;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    @keyframes bounce {
        to {
            transform: translateY(-10px);
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Menambahkan JavaScript untuk peringatan refresh
st.components.v1.html("""
    <script>
    window.onbeforeunload = function() {
        return "Data pada tabel akan hilang jika Anda meninggalkan halaman ini. Apakah Anda yakin?";
    };
    </script>
    """, height=0)

# Inisialisasi DataFrame
if 'df_used_numbers' not in st.session_state:
    st.session_state.df_used_numbers = pd.DataFrame(columns=['No', 'Nomor Peserta Doorprize'])

# Judul aplikasi
# st.title("Pengacakan Penerima Doorprize")

# Durasi total animasi dalam detik
total_duration = 5  # Setel durasi total animasi (misalnya 5 detik)

# Jumlah iterasi animasi
num_iterations = 150

# Hitung waktu tidur per iterasi
sleep_time = total_duration / num_iterations

# Form untuk pengacakan
with st.form(key='doorprize_form', clear_on_submit=True):
    total_numbers = 5000

    if st.form_submit_button("Mulai"):
        available_numbers = list(set(range(1, total_numbers + 1)) - set(st.session_state.df_used_numbers['Nomor Peserta Doorprize']))

        if available_numbers:
            chosen_number = random.choice(available_numbers)
            chosen_number_str = str(chosen_number).zfill(4)

            st.write("Mengacak nomor...")
            placeholder = st.empty()
            for _ in range(num_iterations):
                random_number = random.randint(1, total_numbers)
                random_number_str = str(random_number).zfill(4)
                placeholder.markdown(f"""
                    <div class="number-container">
                        {''.join([f"<div class='random-box'>{digit}</div>" for digit in random_number_str])}
                    </div>
                    """, unsafe_allow_html=True)
                time.sleep(sleep_time)
            
            placeholder.markdown(f"""
                <div class="number-container">
                    {''.join([f"<div class='chosen-box'>{digit}</div>" for digit in chosen_number_str])}
                </div>
                """, unsafe_allow_html=True)
            st.success(f"Nomor yang terpilih: {chosen_number}")

            new_entry = pd.DataFrame({'No': [len(st.session_state.df_used_numbers) + 1], 'Nomor Peserta Doorprize': [chosen_number]})
            st.session_state.df_used_numbers = pd.concat([st.session_state.df_used_numbers, new_entry], ignore_index=True)
        else:
            st.warning("Semua nomor sudah terpilih!")

# Menampilkan daftar nomor yang sudah keluar dalam tabel
st.subheader("Nomor yang sudah terpilih:")
df_used_numbers = st.session_state.df_used_numbers.copy()

# Tampilkan tabel dengan styling
html = df_used_numbers.to_html(index=False, classes='table table-striped')
css = """
    <style>
    .table {
        width: 100%;
        border-collapse: collapse;
    }
    .table th, .table td {
        padding: 8px;
        text-align: left;
        border: 1px solid #ddd;
    }
    .table th {
        background-color: #f4f4f4;
    }
    .table-striped tbody tr:nth-of-type(odd) {
        background-color: #f9f9f9;
    }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)


# Tombol untuk mengunduh CSV
st.subheader("Unduh Data")
csv = df_used_numbers.to_csv(index=False).encode('utf-8')
st.download_button(label="Unduh CSV", data=csv, file_name='doorprize_numbers.csv', mime='text/csv')
