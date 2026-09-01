from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import os
import json

app = Flask(__name__)
app.secret_key = "KAUSHIKSHAURYA"
app.permanent_session_lifetime = timedelta(days=5)


FILE_PATH = "users.json"
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as f:
        USERS = json.load(f)
else:
    USERS = {"dtu_lead": "sih2026"}  # Default user


@app.route("/")
def home():
    curr_user = session.get("username", None)
    return render_template("home2.html", username= curr_user)
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form.get("username")
        password = request.form.get("pass")
        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect(url_for("new_page"))
        elif username not in USERS:
            USERS[username] = password
            return f"New user registered as{username}!"
        else:
            flash("INVALID USERNAME OR PASSWORD!", "danger")
            return redirect(url_for("login"))
    else:
        if "username" in session:
            return redirect(url_for("new_page"))
        return render_template("form.html")
@app.route("/user")
def new_page():
    if "username" in session:
        username = session["username"]
        return f"<h1>Login Successful as {username}</h1>"
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username", None)
        flash("You have been logged out Successfully!", "success")
        return redirect(url_for("home"))
    else:
        return "<h1>Login first! before you Logout!</h1>"
@app.route("/admin")
def admin_panel():
    if session.get("username") != "dtu_lead":
        return "<h3>Access Denied! Only dtu_lead can view this page.</h3><a href='/login'>Login as Admin</a>", 403
    else:
        return render_template("database.html", USERS= USERS)


if __name__ == "__main__":
    app.run(debug=True)