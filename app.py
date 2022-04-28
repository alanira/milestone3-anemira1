"""This app a simple “movie discovery” web app of
randomization choice that shows information about my favorite movies,
and also links to their wikipedia pages"""
import os
import hashlib
import flask
from flask_cors import CORS
from api_set import get_data, get_config
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = flask.Flask(__name__)
CORS(app)

# Point SQLAlchemy to your Heroku database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Gets rid of a warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = os.getenv('secret_key')


db = SQLAlchemy(app)  # db object

bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)


class User(db.Model):
    """ Table user to store username and password"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Review(db.Model):
    """ Table review to store movie id,
    rating, comment and a user name"""
    id = db.Column(db.Integer, primary_key=True)
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
    """This function creating a template using .html file
        and pass values to the variables in a template"""

    if flask.request.method == "POST":
        review_page(flask.request.form)
        return flask.redirect("/loggeduser")

    else:
        name, tagline, genres, poster_path, mov_url, movie_id = get_data()
        base_url, poster_sizes = get_config()
        review = db.engine.execute(
            f""" select * from "review" where movie_id = '{movie_id}' """).all()
        print(review)
        flask.flash(review)
        return flask.render_template(
            ["main.html"],
            name=name,
            tagline=tagline,
            genres=genres,
            poster_path=poster_path,
            base_url=base_url,
            poster_sizes=poster_sizes,
            url=base_url+poster_sizes+poster_path,
            movie_url=mov_url,
            movie_id=movie_id,
        )

# need apply routing to register and login page


@app.route("/register", methods=["POST", "GET"])
def register():
    """This function taking user's input
    as username and password(hashed) and adding it to database.
    If user is already in database(registered)
    then user will be redirected to login page"""
    if flask.request.method == "POST":

        sign_inp = flask.request.form.get("username")
        _pd = flask.request.form.get("password")
        #us = User.query.filter_by(username = login_inp).first()
        db.engine.execute('SELECT * FROM "user";').all()

        if User.query.filter_by(username=sign_inp).first():

            flask.flash('User already present. Try logging in !!')

            return flask.redirect("/")
        else:
            db.session.add(User(username=sign_inp, password=hashlib.md5(
                _pd.encode("utf-8")).hexdigest()))
            db.session.commit()
            flask.flash('User successfully created!!!')
            return flask.redirect("/")

    return flask.render_template(
        ["register.html"],
    )


@app.route("/", methods=["POST", "GET"])
def login():
    """This function taking user's input
    as username and password(will be checked)
    with stored information in DB.
    """
    if flask.request.method == "POST":
        login_inp = flask.request.form.get("username")
        _pd = flask.request.form.get("password")
        pd_hash = hashlib.md5(_pd.encode("utf-8")).hexdigest()
        # us = User.query.filter_by(username = login_inp).first()
        # print(User.query.filter_by(username = login_inp).first())

        if db.engine.execute(
            f""" select * from "user" where username='{login_inp}'
            and password='{pd_hash}' """).all():
            print(db.engine.execute(
                f"""select * from "user" where username='{login_inp}'
                and password='{pd_hash}' """).all())
            return flask.redirect("/loggeduser")
        # if User.query.filter_by(username = login_inp).first() and \
        # User.query.filter_by(password=hashlib.md5(pd.encode("utf-8")).hexdigest()):

        else:
            flask.flash('Username or password is incorrect. Please try again!')
            return flask.redirect("/register")

    return flask.render_template(
        ["login.html"],
    )


@bp.route("/newpage")
def newpage():
    """served by ReactJs
    NB: DO NOT add an "index.html" file in your normal templates folder
    Flask will stop serving this React page correctly"""
    return flask.render_template("index.html")

# CREATED NEW ROUTE for serving React page


@bp.route("/display_fact", methods=["POST", "GET"])
def display_fact():
    """ served by ReactJs
    This function collects all information
    from review DB and returns a dictionary in .json"""
    # display all comments
    usr = flask.request.args.get('user')
    comments = Review.query.filter_by(user=usr).all()
    list_of_reviews = []
    for comment in comments:
        list_of_reviews.append({
            "id": comment.id,
            "movie_id": comment.movie_id,
            "rating": comment.rating,
            "comment": comment.comment,
            "user": comment.user,

        })
    # print(list_of_reviews)
    return flask.jsonify({"comment": list_of_reviews})


app.register_blueprint(bp)

# @app.route("/loggeduser", methods=["POST", "GET"])


def review_page(data):
    """ This function adds movie_id,
    rating, comment and user information
    to review DB"""
    # if flask.request.method == "POST":
    mov_id = dict(data)["MovieID"]
    uname = dict(data)["uname"]
    rating = dict(data)["Rating"]
    comment = dict(data)["Comment"]
    db.session.add(Review(
        movie_id=mov_id,
        rating=rating,
        comment=comment,
        user=uname, ))
    db.session.commit()



@app.route("/update_comments", methods=["POST", "GET"])
def update_comments():
    """ This function updates
    1) edited comments and add them to DB
    2) delete comments by id from DB"""
    res = flask.request.json
    ids = set(res.get("ids")) # all ids that were changed
    del_ids = set(res.get("del_ids")) # list of all deleted comment ids
    data = res.get("data") # all undeleted comment

    for val in ids:
        if val not in del_ids:
            for i in data:

                if int(i["id"]) == int(val):
                    db.engine.execute(
                        f""" update "review" SET Rating = {i["rating"]},
                         Comment = '{(i["comment"])}'  where id = '{val}'  """)
                    break

    for _id in del_ids:
        db.engine.execute(f""" delete from "review" where id = '{_id}' """)

    db.session.commit()

    return flask.jsonify({
        "status": 200,
        "msg": "Data Updated Succesfully"
    })


app.run(debug=True)

# calm-woodland-54914
