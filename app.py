"""This app a simple “movie discovery” web app of 
randomization choice that shows information about my favorite movies,
and also links to their wikipedia pages"""
import os
import flask
import random
from sqlalchemy import PrimaryKeyConstraint
from api_set import get_data, get_config
from flask_sqlalchemy import SQLAlchemy
import hashlib
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#print("app.py=====>",__name__)

app = flask.Flask(__name__)
#print("apppp====",type(app))
# Point SQLAlchemy to your Heroku database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config["SECRET_KEY"]=os.getenv('secret_key')


db = SQLAlchemy(app) # db object

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(1000))
    user = db.Column(db.String(100))

# list_of_reviews = []
# for review in reviews:
#     list_of_reviews.append({
#         "movie_id": review.movie_id,
#     })
db.create_all()   

@app.route("/loggeduser", methods=["POST", "GET"])  # Python decorator
def main():
    if flask.request.method == "POST":
        review_page(flask.request.form)
        return flask.redirect("/loggeduser")
        # return {
        #     "status":"success"
        # },201
        
    else:
        """This function creating a template using .html file
        and pass values to the variables in a template"""
        name, tagline, genres, poster_path, mov_url, movie_id = get_data()
        base_url, poster_sizes = get_config()
        review = db.engine.execute(f""" select * from "review" where movie_id = '{movie_id}' """).all()
        print(review)
        flask.flash(review)
        return flask.render_template(
            ["main.html"],
            name = name,
            tagline = tagline,
            genres = genres,
            poster_path = poster_path,
            base_url = base_url,
            poster_sizes = poster_sizes,
            url=base_url+poster_sizes+poster_path,
            movie_url = mov_url,
            movie_id = movie_id,
            )

#need apply routing to register and login page
@app.route("/register", methods=["POST", "GET"])
def register():
    if flask.request.method == "POST":
        
        sign_inp = flask.request.form.get("username")
        pd = flask.request.form.get("password")
        #us = User.query.filter_by(username = login_inp).first()
        db.engine.execute('SELECT * FROM "user";').all()

        
        if User.query.filter_by(username = sign_inp).first():

            flask.flash('User already present. Try logging in !!')

            return flask.redirect("/")
        else:
            db.session.add(User(username=sign_inp, password=hashlib.md5(pd.encode("utf-8")).hexdigest()))
            db.session.commit()
            flask.flash('User successfully created!!!')
            return flask.redirect("/")
    
    return flask.render_template(
        ["register.html"],
        #log_
        )

@app.route("/", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        login_inp = flask.request.form.get("username")
        pd = flask.request.form.get("password")
        pd_hash=hashlib.md5(pd.encode("utf-8")).hexdigest()
        # us = User.query.filter_by(username = login_inp).first()
        # print(User.query.filter_by(username = login_inp).first())

        if db.engine.execute(f""" select * from "user" where username='{login_inp}' and password='{pd_hash}' """).all() :
            print(db.engine.execute(f"""select * from "user" where username='{login_inp}' and password='{pd_hash}' """).all())
            return flask.redirect("/loggeduser")
        # if User.query.filter_by(username = login_inp).first() and \
        # User.query.filter_by(password=hashlib.md5(pd.encode("utf-8")).hexdigest()):

            
        else:
            print("abracadabra")
            flask.flash('Username or password is incorrect. Please try again!')
            return flask.redirect("/register")
    
    return flask.render_template(
        ["login.html"],
        )

@bp.route("/newpage")
def newpage():
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    print("Hello, Alina!")
    return flask.render_template("index.html")

#CREATED NEW ROUTE for serving React page
@bp.route("/display_fact", methods=["POST","GET"])
def display_fact():
    # display all comments
    comments = Review.query.all()
    #print(return_comments)
    # facts = ["Python was a hobby project", "Python import antigravity", "People prefer Python over French"]
    # fun_fact = random.choice(facts)
    list_of_reviews = []
    
    for comment in comments:
        list_of_reviews.append({
        "movie_id": comment.movie_id,
        "rating": comment.rating,
        "comment": comment.comment,
        "user": comment.user,
        
    })
    print(list_of_reviews)
    return flask.jsonify({"comment": list_of_reviews})

app.register_blueprint(bp)

#@app.route("/loggeduser", methods=["POST", "GET"])
def review_page(data):
    # if flask.request.method == "POST":
    mov_id = dict(data)["MovieID"]
    uname = dict(data)["uname"]
    Rating = dict(data)["Rating"]
    Comment = dict(data)["Comment"]
    db.session.add(Review(
                    movie_id=mov_id,
                    rating=Rating,
                    comment=Comment,
                    user=uname, ))
    db.session.commit()

        #uname = flask.request.form.get("uname")
        # return flask.render_template(
        #     ["index.html"],
        #     uname=uname)


app.run(debug=True)

#calm-woodland-54914