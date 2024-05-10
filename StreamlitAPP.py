import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
from PyPDF2 import PdfReader

#loading json file
#with open('Response.json', 'r') as file:
    #RESPONSE_JSON = json.load(file)


#creating a title for the app
st.title("HPCL Document Management Portal🦜⛓️")


with st.form("user input"):
    uploaded_file = st.file_uploader("Upload PDF or Text")
    subject = st.text_input("Insert Details to be extracted from the file", max_chars=200)
    

    button = st.form_submit_button("Submit")

    if button and uploaded_file is not None and subject:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "subject": subject,
                            
                    
                        }
                    )
                    quiz=response.get("quiz", None)
                st.write(quiz)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            
                    # Extract the quiz data from the response
                    
                   
                