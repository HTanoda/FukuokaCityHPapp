import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

openai.api_key = "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"#st.secrets.OpenAIAPI.openai_api_key

@st.cache
def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join([p.text for p in soup.find_all('p')])

def summarize(text):
    completion = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"次の文章を要約してください：{text}"}
        ],
    )
    return completion['choices'][0]['message']['content']

st.title("福岡市HP要約")

keyword = st.text_input("Enter a keyword")

if keyword:
    url = f"https://www.city.fukuoka.lg.jp/search.html?q={keyword}"  # replace with actual search URL
    data = get_data(url)
    summary = summarize(data)
    
    st.write(summary)
