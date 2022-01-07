from flask import Flask, render_template, request
import requests
import smtplib
from post import Post
from datetime import datetime

year = datetime.now().year
response_data = requests.get("https://api.npoint.io/57b20cb9ccbbf28da6db").json()
MY_EMAIL = "truclhuynh87@gmail.com"
MY_PASSWORD = 'Gookhongbiet88'


response_objects = []
for data in response_data:
    response_obj = Post(data['title'], data['subtitle'], data['author'], data['dates'], data['body'], data['reference'])
    response_objects.append(response_obj)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', all_posts=response_objects)


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def show_contact():
    if request.method == 'POST':
        data_in = request.form
        send_email(data_in["name"], data_in["email"], data_in["phone"], data_in["message"])
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}\n"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        # encrypt the connection, secure it
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs='jackyhuynh87@gmail.com',
            msg=email_message
        )


@app.route('/post/<string:name>')
def show_post(name):
    requested_post = None
    for post in response_objects:
        if post.title == name:
            requested_post = post
    return render_template('post.html', post_obj=requested_post)


@app.route('/entry-form')
def show_entry():
    return render_template('entry-form.html')


if __name__ == '__main__':
    app.run()

