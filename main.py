from flask import Flask, render_template, request
import requests
import smtplib
import os


posts = requests.get("https://api.npoint.io/50ab5f857fd7babb446f").json()
MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]
app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/contact", methods=["POST", "GET"])
def receive_data():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="inopepaul13@gmail.com",
                                msg=f"Subject:\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")
    return render_template("contact.html")




if __name__ == "__main__":
    app.run(debug=True, port=5001)
