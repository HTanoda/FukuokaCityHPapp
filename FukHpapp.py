import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai


# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

@st.cache
def generate_search_query(input_keyword):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"次のキーワードから検索クエリを生成してください：{input_keyword}"}
        ],
    )
    return completion['choices'][0]['message']['content']

@st.cache
def get_search_results(search_query):
    # サイト内検索のURL
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
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"次の文章を要約してください：{content}"}
        ],
    )
    return completion['choices'][0]['message']['content']

# Streamlitアプリの設定
st.title('Search Query Generator and Summarizer')
input_keyword = st.text_input('Enter a keyword')

if st.button('Generate and Summarize'):
    search_query = generate_search_query(input_keyword)
    search_results = get_search_results(search_query)
    summary = summarize_content(search_results)
    st.write(f'Summary: {summary}')
