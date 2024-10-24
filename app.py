import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
import re



st.set_page_config(
    page_title="Multiple Disease Detection",
    page_icon=":hospital",
    layout="wide",
)

with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

diabetes_model = pickle.load(open('saved models/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('saved models/heart_disease_model.sav','rb'))

parkinsons_model = pickle.load(open('saved models/parkinsons_model.sav', 'rb'))


def extract_value_by_keyword(text, keyword):
    pattern = fr"{keyword}\s*:\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        return None



# sidebar for navigation
with st.sidebar:
    
    selected = option_menu('Multiple Disease Prediction System',
                          
                          ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Parkinsons Prediction'],
                          icons=['activity','heart','person'],
                          default_index=0)
    
    
# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    
    # page title
    st.title('Diabetes Prediction using ML')
    diab_diagnosis = ''

    # Option selection: Manual input or PDF upload
    option = st.radio("Select an option:", ("Insert values manually", "Upload a PDF"))

    if option == "Insert values manually":

        # getting the input data from the user        
        col1, col2, col3 = st.columns(3)
        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')
            
        with col2:
            Glucose = st.text_input('Glucose Level')
        
        with col3:
            BloodPressure = st.text_input('Blood Pressure value')
        
        with col1:
            SkinThickness = st.text_input('Skin Thickness value')
        
        with col2:
            Insulin = st.text_input('Insulin Level')
        
        with col3:
            BMI = st.text_input('BMI value')
        
        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
        
        with col2:
            Age = st.text_input('Age of the Person')

        # creating a button for Prediction
    
        if st.button('Diabetes Test Result'):
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            
            if (diab_prediction[0] == 1):
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'
                
            st.success(diab_diagnosis)


    else:

        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()

            # Extract necessary values using keywords
            keywords = {
                "Pregnancy": "pregnancy",
                "Glucose": "glucose",
                "BloodPressure": "bloodpressure",
                "SkinThickness": "skinthickness",
                "Insulin": "insulin",
                "BMI": "bmi",
                "DiabetesPedigreeFunction": "diabetespedigreefunction",
                "Age": "age"
            }

            extracted_data = {}

            for key, keyword in keywords.items():
                value = extract_value_by_keyword(text, keyword)
                if value is not None:
                    extracted_data[key] = value
                else:
                    extracted_data[key] = 1

            # Display the extracted data
            st.write("Extracted Health Data:")
            st.write(extracted_data)

            diab_prediction = diabetes_model.predict([[extracted_data['Pregnancy'], extracted_data['Glucose'], extracted_data['BloodPressure'], extracted_data['SkinThickness'], extracted_data['Insulin'], extracted_data['BMI'], extracted_data['DiabetesPedigreeFunction'], extracted_data['Age']]])
            
            if (diab_prediction[0] == 1):
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'
            
            st.success(diab_diagnosis)



# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):

    # page title
    st.title('Heart Disease Prediction using ML')
    
    option = st.radio("Select an option:", ("Insert values manually", "Upload a PDF"))

    if option == "Insert values manually":
    
        col1, col2, col3 = st.columns(3)
        with col1:
            age = (st.text_input('Age'))
            
        with col2:
            sex = st.text_input('Sex')
            
        with col3:
            cp = st.text_input('Chest Pain types')
            
        with col1:
            trestbps = st.text_input('Resting Blood Pressure')
            
        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')
            
        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
            
        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')
            
        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')
            
        with col3:
            exang = st.text_input('Exercise Induced Angina')
            
        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')
            
        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')
            
        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')
            
        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')


        # code for Prediction
        heart_diagnosis = ''
        
        # creating a button for Prediction
        
        if st.button('Heart Disease Test Result'):
            heart_prediction = heart_disease_model.predict([[float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]])                          
            
            if (heart_prediction[0] == 1):
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'
            
        st.success(heart_diagnosis)

    else:
        # PDF upload form
        st.subheader("Upload a PDF file")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()

            # Extract necessary values using keywords
            keywords = {
                "Age": "age",
                "Sex": "sex",
                "Cp": "cp",
                "Trestbps": "trestbps",
                "Chol": "chol",
                "Fbs": "fbs",
                "Restecg": "restecg",
                "Thalach": "thalach",
                "Exang": "exang",
                "Oldpeak": "oldpeak",
                "Slope": "slope",
                "Ca": "ca",
                "Thal": "thal"
            }

            extracted_data = {}

            for key, keyword in keywords.items():
                value = extract_value_by_keyword(text, keyword)
                if value is not None:
                    extracted_data[key] = float(value)
                else:
                    extracted_data[key] = 1
                    

            # Display the extracted data
            st.write("Extracted Health Data from PDF:")
            st.write(extracted_data)

            heart_prediction = heart_disease_model.predict([[extracted_data['Age'], extracted_data['Sex'], extracted_data['Cp'], extracted_data['Trestbps'], extracted_data['Chol'], extracted_data['Fbs'], extracted_data['Restecg'], extracted_data['Thalach'], extracted_data['Exang'], extracted_data['Oldpeak'], extracted_data['Slope'], extracted_data['Ca'], extracted_data['Thal']]])                          
            
            if (heart_prediction[0] == 1):
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'
            
            st.success(heart_diagnosis)
        
        

# Parkinson's Prediction Page
if (selected == "Parkinsons Prediction"):
    
    # page title
    st.title("Parkinson's Disease Prediction using ML")
    parkinsons_diagnosis = ''
    
    option = st.radio("Select an option:", ("Insert values manually", "Upload a PDF"))

    if option == "Insert values manually":

        col1, col2, col3, col4, col5 = st.columns(5)          
        with col1:
            fo = st.text_input('MDVP: (Fo)')
            
        with col2:
            fhi = st.text_input('MDVP:(Fhi)')
            
        with col3:
            flo = st.text_input('MDVP:(Flow)')
            
        with col4:
            Jitter_percent = st.text_input('MDVP:(Jitter%)')
            
        with col5:
            Jitter_Abs = st.text_input('MDVP:(Jitter Abs)')
            
        with col1:
            RAP = st.text_input('MDVP:(RAP)')
            
        with col2:
            PPQ = st.text_input('MDVP:(PPQ)')
            
        with col3:
            DDP = st.text_input('Jitter:(DDP)')
            
        with col4:
            Shimmer = st.text_input('MDVP:(Shimmer)')
            
        with col5:
            Shimmer_dB = st.text_input('MDVP:(Shimmer dB)')
            
        with col1:
            APQ3 = st.text_input('Shimmer:(APQ3)')
            
        with col2:
            APQ5 = st.text_input('Shimmer:(APQ5)')
            
        with col3:
            APQ = st.text_input('MDVP:(APQ)')
            
        with col4:
            DDA = st.text_input('Shimmer:(DDA)')
            
        with col5:
            NHR = st.text_input('NHR')
            
        with col1:
            HNR = st.text_input('HNR')
            
        with col2:
            RPDE = st.text_input('RPDE')
            
        with col3:
            DFA = st.text_input('DFA')
            
        with col4:
            spread1 = st.text_input('spread1')
            
        with col5:
            spread2 = st.text_input('spread2')
            
        with col1:
            D2 = st.text_input('D2')
            
        with col2:
            PPE = st.text_input('PPE')
            
    
        
        # creating a button for Prediction    
        if st.button("Parkinson's Test Result"):
            parkinsons_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])                          
            
            if (parkinsons_prediction[0] == 1):
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
            
        st.success(parkinsons_diagnosis)

    else:
        # PDF upload form
        st.subheader("Upload a PDF file")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()

            # Extract necessary values using keywords
            keywords = {
            "Fo": "fo",
            "Fhi": "fhi",
            "Flo": "flo",
            "JitterPercent": "jitterpercent",
            "JitterAbs": "jitterabs",
            "RAP": "rap",
            "PPQ": "ppq",
            "DDP": "ddp",
            "Shimmer": "shimmer",
            "ShimmerdB": "shimmerdb",
            "APQ3": "apq3",
            "APQ5": "apq5",
            "APQ": "apq",
            "DDA": "dda",
            "NHR": "nhr",
            "HNR": "hnr",
            "RPDE": "rpde",
            "DFA": "dfa",
            "Spread1": "spread1",
            "Spread2": "spread2",
            "D2": "d2",
            "PPE": "ppe"
            }

            extracted_data = {}

            for key, keyword in keywords.items():
                value = extract_value_by_keyword(text, keyword)
                if value is not None:
                    extracted_data[key] = float(value)
                else:
                    extracted_data[key] = 1
                    

            # Display the extracted data
            st.write("Extracted Health Data from PDF:")
            st.write(extracted_data)

            parkinsons_prediction = parkinsons_model.predict([[extracted_data['Fo'], extracted_data['Fhi'], extracted_data['Flo'], extracted_data['JitterPercent'], extracted_data['JitterAbs'], extracted_data['RAP'], extracted_data['PPQ'], extracted_data['DDP'], extracted_data['Shimmer'], extracted_data['ShimmerdB'], extracted_data['APQ3'], extracted_data['APQ5'], extracted_data['APQ'], extracted_data['DDA'], extracted_data['NHR'], extracted_data['HNR'], extracted_data['RPDE'], extracted_data['DFA'], extracted_data['Spread1'], extracted_data['Spread2'], extracted_data['D2'], extracted_data['PPE']]])

            if (parkinsons_prediction[0] == 1):
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
            
            st.success(parkinsons_diagnosis)


        