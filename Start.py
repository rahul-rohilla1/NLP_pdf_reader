import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import balance_reader as br
import os 
import get_file_path_in_downloads as gfp
import tempfile
import os
import PyPDF2


st.set_page_config(layout="wide")

def home_page():
    st.markdown("""
    <h1 style='text-align: center;'>Welcome to FinInsights 🚀</h1>
    """, unsafe_allow_html=True)
    st.markdown('##')
    st.markdown("""
<div style='text-align: center; font-size: 40px;'> 
Unlock the Power of Financial Analysis with Ease!

<div style='text-align: center; font-size: 20px;'> 
<div style='margin-top: 20px;'>
FinInsights transforms complex company filings into actionable financial insights and recommendations in seconds. Designed for investors who value precision, our app leverages cutting-edge technology to analyze PDF filings, delivering key financial ratios and insights that drive smarter investment decisions.
</div>
""", unsafe_allow_html=True)
   
    st.markdown("""
    <div style='margin-top: 45px;'>
    <div style='text-align: center; font-size: 30px;'>
    How it Works:
    <div style='margin-top: 20px;'>
    <div style='text-align: center; font-size: 20px;'> 
    <b>Upload:</b> Drag and drop any company filing in PDF format.
     <br>
    <b>Analyze:</b> Our AI-powered engine extracts and calculates financial ratios and metrics.
     <br>
    <b>Insights:</b> Get instant access to valuable financial insights and tailored investment recommendations.
     <br>
    <div style='margin-top: 20px;'>
    <div style='text-align: center; font-size: 20px;'>
    Whether you're a seasoned investor or just starting out, FinInsights empowers you with the knowledge you need to identify opportunities and assess risks like never before.
    <div style='margin-top: 20px;'>
    <div style='text-align: center; font-size: 20px;'>
    <b>Start Making Informed Investment Decisions Today!</b>
</div>
""", unsafe_allow_html=True)
    
def doc_upload():
    uploaded_file = st.file_uploader("Choose a file", type=['pdf'])

    if uploaded_file is not None:
        # File has been uploaded, you can now access its details
        file_details = {
            "FileName": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": uploaded_file.size
        }
        full_file_path = gfp(uploaded_file.name)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.getvalue())
        temp_file.close()

        df=br.find_variables(full_file_path)
        st.write(df)
        
    else:
        # No file has been uploaded yet
        st.write("Please upload a file to get started.")
    
    
    
def main():
    # Load data
    pages = {
        "Home Page": home_page,
        "Document Upload": doc_upload
    }

    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox("Select a page:", list(pages.keys()))
    if page in ["Home Page"]:
        pages[page]()  
    else:
        pages[page]()

if __name__ == "__main__":
    main()
else: 
    print("Error: Start.py is not the main file. Please run Start.py to start the app.")