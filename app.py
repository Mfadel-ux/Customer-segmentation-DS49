import streamlit as st
import streamlit.components.v1 as stc
import numpy as np
import pickle

with open('Logistic_Regression_Model.pkl', 'rb') as file:
    Logistic_Regression_Model = pickle.load(file)

html_temp = """<div style="background-color:#000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Customer Segmentation</h1> 
                <h4 style="color:#fff;text-align:center">Made for: Top One</h4> 
                """

desc_temp = """ ### Customer Segmentation 
                This app is used by Credit team for deciding Loan Application
                
                #### Data Source
                Kaggle: Link <Masukkan Link>
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#fff">Customer-segmentation</h1>
                </div
             """
    st.markdown(design, unsafe_allow_html=True)
    Gender = st.selectbox("Gender", ["Male", "Female"]
    ever_married = st.selectbox( "Married?", ["Yes", "No"])
    age = st.slider("Age", 18,100)
    graduated = st.selectbox("Graduate?" ["Yes", "No"])
    profession = st.selectbox("Profession?", ["Engineer", "Doctor", "Lawyer", "Artist"])
    work_exp = st.slider("Work Experience (Year)", 0, 30)
    spending = st.selectbox("Spending Score", ["Low", "Average", "High"]
    family_size = st.slider("Family Size", 1, 10)

    input_data = pd.DataFrame({
        'Gender' : [gender]
        'Ever_Married' :[ever_married]
        'Age' : [age]
        'Graduated' : [graduated]
        'Profession' : [profession]
        'Spending_Score' : [spending]
        'Family_Size' : [family_size]

    })



    #If button is clilcked
     if st.button ("Prediksi")
       prediction = model.predict(input_data)
       st.succes(f"Segmentasi yang diprediksi: {prediction[0]}")

    #Making prediction
    prediction = Logistic_Regression_Model.predict(
        [[Gender, Ever_Married, Age, Graduated, Profession, Spending_Score, Family_Size]] 
    )

    result = "Succes" == 0 else "Not succes"
    return result

if __name__ == "__main__":
    main()
