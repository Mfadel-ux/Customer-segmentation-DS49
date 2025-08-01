import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import numpy as np
import pickle

# Load model
with open('Logistic_Regression_Model.pkl', 'rb') as file:
    model = pickle.load(file)

# HTML Template
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

# Main Function
def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

# ML App
def run_ml_app():
    st.subheader("Predict Segmentasi Pelanggan")

    # Form Input
    gender = st.selectbox("Gender", ["Male", "Female"])
    ever_married = st.selectbox("Married?", ["Yes", "No"])
    age = st.slider("Age", 18, 100)
    graduated = st.selectbox("Graduate?", ["Yes", "No"])
    profession = st.selectbox("Profession?", ["Engineer", "Doctor", "Lawyer", "Artist"])
    work_exp = st.slider("Work Experience (Years)", 0, 30)
    spending = st.selectbox("Spending Score", ["Low", "Average", "High"])
    family_size = st.slider("Family Size", 1, 10)

    # Format ke DataFrame (sesuaikan dengan fitur yang modelmu terima)
    input_data = pd.DataFrame({
        'Gender': [gender],
        'Ever_Married': [ever_married],
        'Age': [age],
        'Graduated': [graduated],
        'Profession': [profession],
        'Work_Experience': [work_exp],
        'Spending_Score': [spending],
        'Family_Size': [family_size]
    })

    if st.button("Prediksi"):
        prediction = model.predict(input_data)
        segmen = prediction[0]

        # IF-ELSE untuk interpretasi hasil
        if segmen == 0:
            st.success("Segmentasi A: Pelanggan Loyal ")
        elif segmen == 1:
            st.info("Segmentasi B: Pelanggan Potensial ")
        elif segmen == 2:
            st.warning("Segmentasi C: Pelanggan Baru ")
        else:
            st.error("Segmentasi D: Kurang Aktif ")

# Run
if __name__ == '__main__':
    main()
