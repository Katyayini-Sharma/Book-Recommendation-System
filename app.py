import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ---------------- Load Data ---------------- #
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

# ---------------- Page Setup ---------------- #
st.set_page_config(page_title="Literary Loft", page_icon="📚", layout="wide")

# ---------------- CSS Styling ---------------- #
st.markdown("""
<style>
/* Body and fonts */
body {
    font-family: 'Open Sans', sans-serif;
    background-color: #f8f8f8;
    color: #333333;
    margin: 0;
    padding: 0;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #2c2c2c;
}

/* Navbar */
.navbar {
    background-color: #ffffff;
    border-bottom: 2px solid #8b4513;
    padding: 10px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
}
.navbar a {
    color: #333333;
    font-weight: 500;
    text-decoration: none;
    font-size: 15px;
}
.navbar a:hover {
    color: #8b4513;
}
.navbar .logo {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 600;
    color: #8b4513;
    margin-right: 30px;
}

/* Card */
.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.08);
    padding: 10px;
    text-align: center;
    margin-bottom: 20px;
}
.card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
}
.card h3 {
    font-size: 16px;
    margin-top: 8px;
}
.card p {
    margin: 4px 0;
    color: #555555;
    font-size: 13px;
}

/* Footer */
footer {
    background-color: #333333;
    color: #f4f4f4;
    text-align: center;
    padding: 20px 0;
    font-size: 14px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Navbar ---------------- #
st.markdown("""
<div class="navbar">
    <div class="logo">Literary Loft</div>
    <a href="#top50">Home</a>
    <a href="#shop">Shop</a>
    <a href="#recommend">Recommend</a>
    <a href="#blog">Blog</a>
    <a href="#contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# ---------------- Sidebar Navigation ---------------- #
page = st.sidebar.radio("Navigate", ["Top 50 Books", "Recommendations"])

# ---------------- PAGE 1: Top 50 Books ---------------- #
if page == "Top 50 Books":
    st.markdown("<h1 id='top50'>Top 50 Book Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    n_cols = 5
    for i in range(0, min(50, len(popular_df)), n_cols):
        cols = st.columns(n_cols)
        for j, col in enumerate(cols):
            if i + j < len(popular_df):
                book = popular_df.iloc[i + j]
                with col:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.image(book['Image-URL-M'], width=120)
                    st.markdown(f"<h3>{book['Book-Title']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p>by <b>{book['Book-Author']}</b></p>", unsafe_allow_html=True)
                    st.markdown(f"<p>Votes: {book['num_ratings']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p>Rating: {round(book['avg_rating'],1)}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PAGE 2: Recommendations ---------------- #
elif page == "Recommendations":
    st.markdown("<h1 id='recommend'>Get Book Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

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
                n_cols = 5
                for i in range(0, len(data), n_cols):
                    cols = st.columns(n_cols)
                    for j, col in enumerate(cols):
                        if i + j < len(data):
                            with col:
                                st.markdown("<div class='card'>", unsafe_allow_html=True)
                                st.image(data[i + j][2], width=120)
                                st.markdown(f"<h3>{data[i + j][0]}</h3>", unsafe_allow_html=True)
                                st.markdown(f"<p>by <b>{data[i + j][1]}</b></p>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No similar books found. Try another one!")

# ---------------- Footer ---------------- #
st.markdown("""
<footer>
    © 2025 Literary Loft. All rights reserved.
</footer>
""", unsafe_allow_html=True)
