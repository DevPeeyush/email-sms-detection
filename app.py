import streamlit as st
import pickle
import sklearn
import nltk
import nltk

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer  
import string

ps = PorterStemmer()

def transformed_text(text):
    # .lower is used to convert sentence in the lower case
    text = text.lower()
    # nltk.word_tokenizer(text) convert sentence into list 
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

tfidf_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title('Email-Sms Spam Detection')

input_sms = st.text_input('Enter the message:')

if st.button('Predict'):
    # 1. Preprocessing
    transform_sms = transformed_text(input_sms)
    # 2. Vectorize
    vector_input = tfidf_vectorizer.transform([transform_sms])
    # 3. Predict
    prediction = model.predict(vector_input.toarray())[0]
    # Display
    if prediction == 1:
        st.header("SPAM")
    else:
        st.header("NOT SPAM")

