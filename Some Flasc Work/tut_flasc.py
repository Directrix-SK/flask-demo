from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/wtf")
def new_page():
    return "This is the new page of my website! <h1><font color = blue>NICE BRO</font><h1>"
@app.route("/admin")
def admin():
    return redirect(url_for("new_page"))
@app.route("/RUHAAN")
def ruhaan():
    return render_template("Ruhaan.html")
@app.route("/SAMPADA")
def sampada():
    return render_template("Sampada.html")
@app.route("/NAVYA")
def navya():
    return render_template("Navya.html")
@app.route("/SARTHAK")
def sarthak():
    return render_template("Sarthak.html")
@app.route("/RIDDHIMA")
def riddhima():
    return render_template("Riddhima.html")
@app.route("/KAUSHIK")
def kaushik():
    return render_template("Kaushik.html")
@app.route("/<name>")
def same(name):
    return render_template("justonetime.html", content = name)
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug=True)