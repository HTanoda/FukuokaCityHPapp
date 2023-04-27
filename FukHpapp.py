import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

@st.cache
def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join([p.text for p in soup.find_all('p')])

def summarize(text):
    completion = openai.Completion.create(engine="gpt-3.5-turbo", prompt=f"{text}\n\nSummarize:", max_tokens=60)
    return completion.choices[0].text.strip()

st.title("Fukuoka City Information Summarizer")

keyword = st.text_input("Enter a keyword")

if keyword:
    url = f"https://www.city.fukuoka.lg.jp/search.html?q={keyword}"  # replace with actual search URL
    data = get_data(url)
    summary = summarize(data)
    
    st.write(summary)
