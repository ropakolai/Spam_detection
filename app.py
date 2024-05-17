# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZaPD3g-zTwW-Grczb7cciMyvlor0O23J
"""



import streamlit as st
import joblib
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.download('punkt')

# Load vectorizers and models
vectorizer_lgrg = joblib.load('models/tfidf_vectorizer_lgrg.pkl')
model_lgrg = joblib.load('models/lgrg_model.pkl')

vectorizer_mnnb = joblib.load('models/tfidf_vectorizer_mnnb.pkl')
model_mnnb = joblib.load('models/mnnb_model.pkl')

vectorizer_svc = joblib.load('models/svc_model.pkl')
model_svc = joblib.load('models/tfidf_vectorizer_svc.pkl')

# Initialize the stemmer
stemmer = PorterStemmer()

# Define the list of vectorizers
vectorizers = [vectorizer_lgrg, vectorizer_svc, vectorizer_mnnb]

# List of models and associated vectorizers
model_names = ['Logistic Regression', 'SVC', 'Multinomial Naive Bayes']
models = [model_lgrg, model_svc, model_mnnb]

# Stemming function
def stem_text(text):
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)

# Prediction function
def predict(text):
    text_stemmed = stem_text(text)
    predictions = []
    for vectorizer, model in zip(vectorizers, models):
        text_vectorized = vectorizer.transform([text_stemmed])
        prediction = model.predict(text_vectorized)[0]
        predictions.append(prediction)
    return predictions

# Streamlit user interface
st.title('Spam Detection')
st.write("This Streamlit project provides a user interface for spam detection using machine learning models. "
         "It allows users to input text for classification as spam or non-spam. "
         "The application utilizes natural language processing (NLP) techniques such as tokenization and stemming, "
         "alongside pre-trained models like Logistic Regression, Support Vector Machine, and Multinomial Naive Bayes.")
col1, col2 = st.columns(2)
col1.image('src/not_spam.png', use_column_width=True)
col2.image('src/spam.png', use_column_width=True)


# User input
user_input = st.text_area('Enter the text to classify as spam or non-spam')

st.write("A few examples if you lack of imagination :)")

# Table of examples

table_data = {
    'Examples': [
        "Santa Calling! Would your little ones like a call from Santa Xmas eve? Call 09058094583 to book your time.",
        "For the most sparkling shopping breaks from 45 per person; call 0121 2025050 or visit www.shortbreaks.org.uk",
        "... Are you in the pub?",
        "hows my favourite person today? r u workin hard? couldn't sleep again last nite nearly rang u at 4.30"
    ]
}
st.table(table_data)

# Button to perform prediction
if st.button('Classify'):
    if user_input:
        # Prediction
        st.write("Prediction:")
        for vectorizer, model, model_name in zip(vectorizers, models, model_names):
            text_stemmed = stem_text(user_input)
            text_vectorized = vectorizer.transform([text_stemmed])
            prediction = model.predict(text_vectorized)[0]
            st.write(f"{model_name}: Prediction: {prediction}")
    else:
        st.warning('Please enter text to classify.')
