from flask import Flask, render_template, request
import requests
from post import Post
from datetime import datetime

year = datetime.now().year
response_data = requests.get("https://api.npoint.io/57b20cb9ccbbf28da6db").json()
response_objects = []
for data in response_data:
    response_obj = Post(data['title'], data['subtitle'], data['author'], data['dates'], data['body'])
    response_objects.append(response_obj)
print(response_objects)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', all_posts=response_objects)


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/contact')
def show_contact():
    return render_template('contact.html')


@app.route('/post/<string:name>')
def show_post(name):
    requested_post = None
    for post in response_objects:
        if post.title == name:
            requested_post = post
    return render_template('post.html', post_obj=requested_post)


@app.route('/form-entry', methods=['POST'])
def receive_data():
    data = request.form
    print(data["name"])
    print(data["email"])
    print(data["phone"])
    print(data["message"])
    return render_template('entry-form.html')


if __name__ == '__main__':
    app.run()

