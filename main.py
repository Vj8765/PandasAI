import os
import openai
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib

matplotlib.use('Tkagg')

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai.api_key)

st.title("Welcome To PandasAI 🐼")

uploaded_file = st.file_uploader("Upload a CSV or Excel file for Analysis", type=['csv', 'xlsx'])

if uploaded_file is not None:
    file_extension = os.path.splitext(uploaded_file.name)[1]
    
    if file_extension == '.csv':
        df = pd.read_csv(uploaded_file)
    elif file_extension == '.xlsx':
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    sdf = SmartDataframe(df, config={"llm": llm})
    prompt = st.text_area("Enter your prompt:", placeholder="Type your question here...")
    
    if st.button("Generate", key="generate_button"):
        if prompt:
            with st.spinner("Generating response. . ."):
                response = sdf.chat(prompt)
                st.success(response)
                    
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()
        else:
            st.warning("Please enter a prompt.")
