import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Analisis Sentimen Twitter")


st.markdown("#### Pada analisis kali ini penulis mengambil topik 'polisi', dimana topik ini sedang menjadi perbincangan hangat di kalangan masyarakat baik di portal berita maupun di media sosial khususnya twitter. ")


data_path = ("C:\\Users\\Gian\\tweet_clean.csv")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(data_path)
    return data


data = load_data()

st.sidebar.subheader("Pilih Contoh Tweet")
random_tweet = st.sidebar.radio('Jenis Sentimen',('positif','negatif','netral'))

st.markdown("### Contoh Tweet: ")

st.markdown(data.query("sentiment == @random_tweet")[['tweet']].sample(n=1).iat[0,0])

st.sidebar.subheader("Jumlah Tweet")
select = st.sidebar.selectbox('Jenis Visualisasi',['Histogram','PieChart'])

sentiment_count = data['sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiments':sentiment_count.index,'Tweets':sentiment_count.values})

if st.sidebar.checkbox('Show',False,key='0'):
    st.markdown("### Jumlah Tweet Berdasarkan Sentimen")
    if select=='Histogram':
        fig = px.bar(sentiment_count,x='Sentiments',y='Tweets',color='Tweets',height=200)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count,values='Tweets',names='Sentiments')
        st.plotly_chart(fig)


    # Word cloud
st.sidebar.subheader("Word Cloud")
st.set_option('deprecation.showPyplotGlobalUse', False)
word_sentiment = st.sidebar.radio("Jenis Sentiment", tuple(pd.unique(data["sentiment"])))
if st.sidebar.checkbox("Show", False, key="6"):
    st.subheader(f"Word Cloud Untuk Sentimen {word_sentiment.capitalize()} ")
    df = data[data["sentiment"]==word_sentiment]
    words = " ".join(df["clean_tweet"].apply(str))
    processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

