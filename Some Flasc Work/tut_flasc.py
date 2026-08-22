from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/wtf")
def new_page():
    return "This is the new page of my website! <h1><font color = blue>NICE BRO</font><h1>"
@app.route("/<name>")
def user(name: str):
    act_name = name.capitalize()
    return f"Hello {act_name}, Welcome to the web server!!!"
@app.route("/admin")
def admin():
    return redirect(url_for("new_page"))
@app.route("/RUHAAN")
def ruhaan():
    return render_template("Ruhaan.html")
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug=True)