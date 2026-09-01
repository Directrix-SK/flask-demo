from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home2.html")
@app.route("/login")
def login():
    return render_template("form.html")
@app.route("/new", methods=["POST"])
#i want that /new page to be only accessed when user hits the submit button not 
# from the /new at the address bar, so i can put the method to be 
# accessed for the new page, that method = ["POST"], and bt writing only post, i can guarantee that no one can enter
#  my new page from /new because this which we type in the address bar is a get command not a post and post is only 
# accessible for when i hit the submit button present on the login form
def new_page():
    user_input = request.form.get("username")
    return render_template("done.html", user = user_input)

if __name__ == "__main__":
    app.run(debug=True)