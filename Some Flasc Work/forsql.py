from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "KAUSHIKSHAURYA"
app.permanent_session_lifetime = timedelta(days=5)



@app.route("/")
def home():
    curr_user = session.get("username", None)
    return render_template("home2.html", username= curr_user)
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        
        return redirect(url_for("home"))
    else:
        if "username" in session:
            return redirect(url_for("new_page"))
        else:
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
        session.pop("password", None)
        flash("You have been logged out Successfully!", "success")
        return redirect(url_for("home"))
    else:
        return "<h1>Login first! before you Logout!</h1>"

if __name__ == "__main__":
    app.run(debug=True)