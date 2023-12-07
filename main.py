from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from movie_api import *
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chinaaa'
Bootstrap5(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies.db"
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.Text)
    img_url = db.Column(db.String(250))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movie = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars()
    return render_template("index.html", movies=movie)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        print(movie_id)
        movie_to_update = db.get_or_404(Movie, movie_id)
        if request.form['new_rating']:
            movie_to_update.rating = request.form['new_rating']
        if request.form['rank']:
            movie_to_update.ranking = request.form['rank']
        if request.form['new_review']:
            movie_to_update.review = request.form['new_review']
        db.session.commit()
        return redirect(url_for('home'))

    movie_id = request.args.get('id')
    movie_to_edit = db.get_or_404(Movie, movie_id)
    return render_template('edit.html', movie=movie_to_edit)


@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        search_all_movies(request.form['movie_title'])
        return redirect(url_for('select'))
    return render_template('add.html')

@app.route('/select')
def select():
    movie_title = request.args.get('title')
    if movie_title:
        new_movie = Movie()
        new_movie.title = request.args.get('title')
        new_movie.year = request.args.get('year').split('-')[0]
        new_movie.description = request.args.get('overview')
        new_movie.rating = request.args.get('rating')
        new_movie.img_url = f"https://image.tmdb.org/t/p/original/{request.args.get('image')}"
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))


    with open('movies.json', 'r') as file:
        movies = json.load(file)

    return render_template('select.html', movies=movies['results'])


if __name__ == '__main__':
    app.run(debug=True)
