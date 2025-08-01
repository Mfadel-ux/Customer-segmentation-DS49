import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# --- Bagian 1: Memuat Model ---
try:
    with open('Logistic_Regression_Model.pkl', 'rb') as file:
        Logistic_Regression_Model.pkl = pickle.load(file)
except FileNotFoundError:
    st.error("Error: Model file 'Logistic_Regression_Model.pkl' not found.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- Bagian 2: Tampilan HTML dan Deskripsi ---
html_temp = """
<div style="background-color:#000;padding:10px;border-radius:10px">
    <h1 style="color:#fff;text-align:center">Customer Segmentation</h1>
    <h4 style="color:#fff;text-align:center">Made for: Top One</h4>
</div>
"""

desc_temp = """
### Customer Segmentation
This app is used by Credit team for deciding Loan Application

#### Data Source
Kaggle: Link <Masukkan Link>
"""

# --- Bagian 3: Fungsi Utama Aplikasi ---
def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

# --- Bagian 4: Aplikasi Machine Learning ---
def run_ml_app():
    st.subheader("Prediksi Segmentasi Pelanggan")

    # --- INPUT DARI PENGGUNA ---
    # Masukkan semua fitur yang relevan di sini.
    # Jika ada kolom 'Var_1', Anda harus memasukkan input untuk itu juga.
    gender = st.selectbox("Gender", ["Male", "Female"])
    ever_married = st.selectbox("Married?", ["Yes", "No"])
    age = st.slider("Age", 18, 100)
    graduated = st.selectbox("Graduated?", ["Yes", "No"])
    profession = st.selectbox("Profession?", ['Artist', 'Healthcare', 'Entertainment', 'Engineer', 'Doctor', 'Lawyer', 'Executive', 'Homemaker'])
    work_exp = st.slider("Work Experience (Years)", 0, 30)
    spending = st.selectbox("Spending Score", ["Low", "Average", "High"])
    family_size = st.slider("Family Size", 1, 10)
    var_1 = st.selectbox("Var_1", ['CAT_4', 'CAT_3', 'CAT_1', 'CAT_2', 'CAT_6', 'CAT_5', 'CAT_7'])
    
    # --- PROSES INPUT UNTUK MODEL ---
    # Kami akan meniru pipeline preprocessing yang kemungkinan besar Anda gunakan
    # saat melatih model.
    if st.button("Prediksi"):
        # 1. Buat DataFrame dari input pengguna
        input_df = pd.DataFrame([{
            'Gender': gender,
            'Ever_Married': ever_married,
            'Age': age,
            'Graduated': graduated,
            'Profession': profession,
            'Work_Experience': work_exp,
            'Spending_Score': spending,
            'Family_Size': family_size,
            'Var_1': var_1,
        }])
        
        # 2. Lakukan Label Encoding untuk kolom biner
        le = LabelEncoder()
        binary_cols = ['Gender', 'Ever_Married', 'Graduated']
        for col in binary_cols:
            # Note: Anda perlu menggunakan le.fit_transform() karena Anda tidak
            # menyimpan dan memuat preprocessor-nya. Ini OK untuk biner.
            input_df[col] = le.fit_transform(input_df[col])
            # Pastikan kategori yang diencode sesuai dengan yang dilatih.
            # Misalnya, Male=1, Female=0
            
        # 3. Lakukan One-Hot Encoding untuk kolom multi-kategori
        # Ini akan menghasilkan kolom dummy baru dengan drop_first=True
        categorical_cols_for_ohe = ['Profession', 'Spending_Score', 'Var_1']
        input_df_encoded = pd.get_dummies(input_df, columns=categorical_cols_for_ohe, drop_first=True)

        # 4. Pastikan semua kolom yang dibutuhkan model ada, bahkan jika kategorinya tidak dipilih.
        # Ini adalah langkah KRITIS untuk memastikan kolom input sama persis dengan kolom training.
        # Anda harus membuat daftar semua kolom yang diharapkan oleh model (misalnya, dari X_train.columns).
        # Saya akan membuat contoh daftar kolom untuk demonstrasi.
        expected_cols = [
            'Gender', 'Ever_Married', 'Age', 'Graduated', 'Work_Experience',
            'Family_Size',
            'Profession_Doctor', 'Profession_Entertainment', 'Profession_Executive',
            'Profession_Healthcare', 'Profession_Homemaker', 'Profession_Lawyer',
            'Spending_Score_High', 'Spending_Score_Low',
            'Var_1_CAT_2', 'Var_1_CAT_3', 'Var_1_CAT_4', 'Var_1_CAT_5', 'Var_1_CAT_6', 'Var_1_CAT_7'
        ]

        # Tambahkan kolom yang hilang dan isi dengan 0
        for col in expected_cols:
            if col not in input_df_encoded.columns:
                input_df_encoded[col] = 0
        
        # Urutkan kembali kolom agar sesuai dengan urutan yang digunakan saat melatih model
        input_final = input_df_encoded[expected_cols]

        try:
            # 5. Prediksi menggunakan model
            prediction = model.predict(input_final)
            segmen = prediction[0]

            # --- TAMPILKAN HASIL ---
            # IF-ELSE untuk interpretasi hasil
            if segmen == 0:
                st.success("Segmentasi A: Pelanggan Loyal ")
            elif segmen == 1:
                st.info("Segmentasi B: Pelanggan Potensial ")
            elif segmen == 2:
                st.warning("Segmentasi C: Pelanggan Baru ")
            else:
                st.error("Segmentasi D: Kurang Aktif ")
        except Exception as e:
            st.error(f"Error saat prediksi: {e}")
            st.write("Pastikan kolom-kolom input yang dikirim ke model sudah benar.")
            st.write("Kolom yang dikirim:")
            st.write(input_final)

# --- Bagian 5: Menjalankan Aplikasi ---
if __name__ == '__main__':
    main()
