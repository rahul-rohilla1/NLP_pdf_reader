import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import balance_reader as br
import tempfile
import os
import time
import financial_ratios as fr

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
    st.write("hi")
    
def doc_upload():
    st.header('Compare 2 companies', divider='rainbow')
    st.write("To get started upload 2 Balance Sheet file")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file_1 = st.file_uploader("Financial Document 1", type=['pdf'])

     
    with col2:
        uploaded_file_2 = st.file_uploader("Financial Document 2", type=['pdf'])

    if uploaded_file_2 is not None and uploaded_file_1 is not None:
        file_details_1 = {
                "FileName": uploaded_file_1.name,
                "FileType": uploaded_file_1.type,
                "FileSize": uploaded_file_1.size
            }    
        temp_file_1 = tempfile.NamedTemporaryFile(delete=False)
        temp_file_1.write(uploaded_file_1.getvalue())
        temp_file_1.close()

        file_details_2 = {
                "FileName": uploaded_file_2.name,
                "FileType": uploaded_file_2.type,
                "FileSize": uploaded_file_2.size
            }
            
        temp_file_2 = tempfile.NamedTemporaryFile(delete=False)
        temp_file_2.write(uploaded_file_2.getvalue())
        temp_file_2.close()
        with st.spinner('Be patient, we are analyzing the documents ...'):
            merged_df_1=fr.ratios(temp_file_2.name)
            merged_df_2=fr.ratios(temp_file_1.name)
            
            st.write(merged_df_1)
            st.write(merged_df_2)

        st.success('Done!')
    
    
        
      
    
def main():
    # Load data
    pages = {
        "Home Page": home_page,
        "Document Upload": doc_upload
    }
    st.sidebar.image("pics/logo.jpeg", use_column_width=True)
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