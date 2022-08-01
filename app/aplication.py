from flask import Flask, abort, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(80))
    body = db.Column(db.String(200))

    def dict_from_post(self):
        return {"id": self.id, "userId": self.userId,
                "title": self.title, "body": self.body}


@app.get("/posts")
def get_all_posts():
    user_id = request.args.get("userId")
    if user_id is None:
        posts = Post.query.all()
    else:
        posts = Post.query.filter(Post.userId == user_id).all()
    result = []
    for post in posts:
        post_dictionary = post.dict_from_post()
        result.append(post_dictionary)
    return {"posts": result}


@app.get("/posts/<id>")
def get_post(id):
    external_url = "https://jsonplaceholder.typicode.com/posts/" + str(id)
    post = Post.query.get(id)
    if post is None:
        response = requests.get(external_url)
        if response.status_code == 404:
            abort(404)
        external_post = response.json()
        return upload_post(create_post_id(
            external_post["id"],
            external_post["userId"],
            external_post["title"],
            external_post["body"]))
    return post.dict_from_post()


def create_post_id(id, user_id, title, body):
    post = Post(id=id, userId=user_id, title=title, body=body)
    return post


def create_post(user_id, title, body):
    post = Post(userId=user_id, title=title, body=body)
    return post


def upload_post(post):
    db.session.add(post)
    db.session.commit()
    return post.dict_from_post()


def check_user_id(user_id):
    external_url = "https://jsonplaceholder.typicode.com/users/" + str(user_id)
    user_response = requests.get(external_url)
    if user_response.status_code == 404:
        return False
    return True


@app.post("/posts")
def post_post():
    json = request.json
    post = ""
    try:
        user_id = json['userId']
        if not check_user_id(user_id):
            return "Bad user id", 400
        post = upload_post(
            create_post(json['userId'], json['title'],
                        json['body']))

    except KeyError:
        abort(400)

    return post


@app.delete("/posts/<id>")
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return "success"


@app.patch("/posts/<id>")
def update_post(id):
    post = Post.query.get_or_404(id)
    args = request.args
    new_title = args.get("title")
    if new_title is not None:
        post.title = new_title
    new_body = args.get("body")
    if new_body is not None:
        post.body = new_body
    db.session.commit()
    return post.dict_from_post()


@app.route('/')
def home():
    return render_template("index.html"), 200


if __name__ == '__main__':
    app.run()
