import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

# Page setup
st.set_page_config(page_title="Literary Loft", layout="wide")
st.title("📚 Literary Loft - Book Recommender")

# Show popular books
st.subheader(" Top 10 Popular Books")
cols = st.columns(5)
for i, col in enumerate(cols * 2):  # top 10
    if i < len(popular_df):
        book = popular_df.iloc[i]
        with col:
            st.image(book['Image-URL-M'], width=120)
            st.markdown(f"**{book['Book-Title']}**")
            st.markdown(f"*by {book['Book-Author']}*")
            st.markdown(f"⭐ {book['avg_rating']} | {book['num_ratings']} ratings")

# Recommendations input
st.subheader("Get Recommendations")
user_input = st.text_input("Enter a book you like:")

if st.button("Recommend"):
    if user_input not in pt.index:
        st.warning(f"Sorry, we couldn’t find the book “{user_input}”. Check spelling or try another.")
    else:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:11]

        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            if not temp_df.empty:
                data.append([
                    temp_df['Book-Title'].values[0],
                    temp_df['Book-Author'].values[0],
                    temp_df['Image-URL-M'].values[0]
                ])

        if data:
            st.subheader("Recommended Books")
            cols = st.columns(5)
            for i, col in enumerate(cols * 2):
                if i < len(data):
                    with col:
                        st.image(data[i][2], width=120)
                        st.markdown(f"**{data[i][0]}**")
                        st.markdown(f"*by {data[i][1]}*")
        else:
            st.warning("No similar books found. Try another one!")
