import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI, ChatCompletion


# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# GPT-3の設定
gpt3 = ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Translate this English text to French: {input_text}"}
    ]
)

@st.cache
def generate_search_query(input_keyword):
    # GPT-3を使用して検索クエリを生成
    response = gpt3.complete(prompt=f"Generate a search query for the keyword: {input_keyword}")
    return response.choices[0].text.strip()

@st.cache
def get_search_results(search_query):
    # サイト内検索のURL (この例ではGoogleを使用)
    search_url = f"https://www.city.fukuoka.lg.jp//search/search.html?q={search_query}"
    
    # ページの内容を取得
    page = requests.get(search_url)
    
    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(page.content, "html.parser")
    
    # 最初の検索結果を取得
    first_result = soup.find_all('div', class_='g')[0].text
    
    return first_result

@st.cache
def summarize_content(content):
    # GPT-3を使用して内容を要約
    response = gpt3.complete(prompt=f"Summarize the following content: {content}")
    return response.choices[0].text.strip()

# Streamlitアプリの設定
st.title('Search Query Generator and Summarizer')
input_keyword = st.text_input('Enter a keyword')

if st.button('Generate and Summarize'):
    search_query = generate_search_query(input_keyword)
    search_results = get_search_results(search_query)
    summary = summarize_content(search_results)
    st.write(f'Summary: {summary}')
