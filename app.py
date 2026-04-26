import requests
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, jsonify
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key is required for session management (login/logout)
app.config['SECRET_KEY'] = 'realtime-api-project-2026'

# SQLite is used here for simplicity and fast local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# External movie API configuration (TMDB)
API_KEY = 'c6897e4cd5dfd707bfaa571c4fbcbb6c'
BASE_URL = "https://api.themoviedb.org/3"

# Database Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique so it can safely identify a reviewer
    username = db.Column(db.String(50), unique=True, nullable=False)

    # Password is stored as a hash for security reasons
    password = db.Column(db.String(100), nullable=False)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Links review to a specific TMDB movie without duplicating movie data locally
    tmdb_id = db.Column(db.Integer, nullable=False)

    username = db.Column(db.String(50), nullable=False)

# API Routes

@app.route('/api/movies/search')
def search_api():
    query = request.args.get('q')

    if not query:
        return jsonify([])

    try:
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
        data = requests.get(url, timeout=5).json()

        # Limit results to keep autocomplete fast and lightweight
        return jsonify(data.get('results', [])[:8])

    except Exception:
        # Fail silently to avoid breaking frontend autocomplete experience
        return jsonify([])

# Page Routes

@app.route('/')
def index():
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&page=1"
    movies = []

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            movies = response.json().get('results', [])[:10]

    except Exception as e:
        print(f"Homepage Fetch Error: {e}")

    return render_template('index.html', movies=movies)


@app.route('/movie/<int:tmdb_id>', methods=['GET', 'POST'])
def movie_detail(tmdb_id):
    url = f"{BASE_URL}/movie/{tmdb_id}?api_key={API_KEY}"
    movie = requests.get(url).json()

    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))

        review = Review(
            content=request.form['content'],
            rating=int(request.form['rating']),
            tmdb_id=tmdb_id,
            username=session['username']
        )

        db.session.add(review)
        db.session.commit()

        return redirect(url_for('movie_detail', tmdb_id=tmdb_id))

    reviews = Review.query.filter_by(tmdb_id=tmdb_id).all()

    avg = (
        round(sum(r.rating for r in reviews) / len(reviews), 1)
        if reviews else "N/A"
    )

    return render_template(
        'movie_detail.html',
        movie=movie,
        reviews=reviews,
        avg_rating=avg
    )


@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    review = Review.query.get_or_404(review_id)

    # Prevent users from deleting reviews they don't own
    if review.username != session['username']:
        return redirect(url_for('movie_detail', tmdb_id=review.tmdb_id))

    db.session.delete(review)
    db.session.commit()

    return redirect(url_for('movie_detail', tmdb_id=review.tmdb_id))

# Auth Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])

        user = User(
            username=request.form['username'],
            password=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', hide_navbar=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username']
        ).first()

        if user and check_password_hash(user.password, request.form['password']):
            session['username'] = user.username
            return redirect(url_for('index'))

    return render_template('login.html', hide_navbar=True)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# App Entry Point

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)