# from flask import Flask, render_template, request
# import pickle

# app = Flask(__name__)

# # Load the pickled movie data and similarity scores
# movies = pickle.load(open('./model/movie_list.pkl', 'rb'))
# similarity = pickle.load(open('./model/similarity.pkl', 'rb'))

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     movie_name = request.form.get('movie_name')
    
#     # Find the index of the movie in the dataset
#     index = movies[movies['title'] == movie_name].index[0]
    
#     # Get similarity scores and sort them
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
#     # Get the top 5 recommendations
#     recommended_movies = [movies.iloc[i[0]].title for i in distances[1:6]]
    
#     return render_template('index.html', movie_name=movie_name, recommendations=recommended_movies)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the pickled movie data and similarity scores
movies = pickle.load(open('./model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('./model/similarity.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form.get('movie_name')
    
    # Find the index of the movie in the dataset
    try:
        index = movies[movies['title'] == movie_name].index[0]
    except IndexError:
        return render_template('index.html', movie_name=movie_name, recommendations=[], error="Movie not found.")

    # Get similarity scores and sort them
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    # Get the top 5 recommendations with details
    recommended_movies = []
    for i in distances[1:6]:
        movie_details = {
            'title': movies.iloc[i[0]]['title'],
            'tags': movies.iloc[i[0]]['tags'],  # Assuming 'tags' includes the tagline
            'genres': movies.iloc[i[0]]['genres'],
            'cast': movies.iloc[i[0]]['cast'],
            'crew': movies.iloc[i[0]]['crew']
        }
        recommended_movies.append(movie_details)

        
    return render_template('index.html', movie_name=movie_name, recommendations=recommended_movies)


if __name__ == '__main__':
    app.run(debug=True)