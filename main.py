import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from PyPDF2 import PdfReader

st.title("Text Summarizer")

@st.cache_resource
def load_model_and_tokenizer():
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model_and_tokenizer()

def summarize_text(text, max_length=150, min_length=50):
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs["input_ids"], num_beams=4, min_length=min_length, max_length=max_length, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

input_option = st.radio("Choose input type:", ("Enter Text", "Upload PDF"))

if input_option == "Enter Text":
    text_input = st.text_area("Enter the text you want to summarize:")
    if st.button("Summarize Text"):
        if text_input:
            summary = summarize_text(text_input)
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter some text to summarize.")

else:
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        if st.button("Summarize PDF"):
            text = extract_text_from_pdf(uploaded_file)
            summary = summarize_text(text)
            st.subheader("Summary:")
            st.write(summary)