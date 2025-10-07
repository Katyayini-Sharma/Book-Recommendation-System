from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load models and data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    try:
        # Check if the book exists in the pivot table index
        if user_input not in pt.index:
            message = f"Sorry, we couldn’t find the book “{user_input}”. Please check the spelling or try another title."
            return render_template('recommend.html', message=message)

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

        if not data:
            message = f"Sorry, no similar books found for “{user_input}”. Try another one!"
            return render_template('recommend.html', message=message)

        return render_template('recommend.html', data=data)

    except Exception as e:
        print("Error:", e)
        message = "Oops! Something went wrong while fetching recommendations. Please try again later."
        return render_template('recommend.html', message=message)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
