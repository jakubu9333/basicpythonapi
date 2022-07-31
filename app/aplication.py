from flask import Flask, abort,request
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
    posts = Post.query.all()
    result = []
    for post in posts:
        post_dictionary = post.dict_from_post()
        result.append(post_dictionary)
    return {"posts": result}


@app.get("/posts/<id>")
def get_post(id):
    external_uri = "https://jsonplaceholder.typicode.com/posts/" + str(id)
    post = Post.query.get(id)
    if post is None:
        response = requests.get(external_uri)
        if response.status_code == 404:
            abort(404)
        response_json = response.json()
        return upload_post(create_post_id(
            response_json["id"],
            response_json["userId"],
            response_json["title"],
            response_json["body"]))
    return post.dict_from_post()


def create_post_id(id, userId, title, body):
    post = Post(id=id, userId=userId, title=title, body=body)
    return post


def create_post(user_id, title, body):
    post = Post(userId=user_id, title=title, body=body)
    return post


def upload_post(post):
    db.session.add(post)
    db.session.commit()
    return post.dict_from_post()


@app.post("/posts")
def post_post():
    json= request.json
    post=""
    try:
        post = upload_post(
        create_post(request.json['userId'], request.json['title'],
                request.json['body']))

    except KeyError:
        abort(400)

    return post


@app.delete("/posts/<id>")
def delete_post(id):
    result = Post.query.delete()
    return "success"


@app.put("/posts/<id>")
def update_post():
    return "success"


@app.route('/')
def home():
    return "xd"


if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()
