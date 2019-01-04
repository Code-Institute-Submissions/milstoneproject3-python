import os
from flask import Flask, render_template,request, session,url_for, redirect

app = Flask(__name__)
app.secret_key = ("this is super secret")


@app.route("/", methods=["GET","POST"])
#  route to homepage
def index():
    if request.method =="POST":
        session["username"] = request.form["username"]
        
    if "username" in session:
        return redirect(url_for("user", username=session["username"]))
        
    return render_template("index.html")
    
@app.route("/<username>")
# route to userpage
def user(username):
    return "This is a page for:" + username

@app.route("/<username>/riddles")
# route to riddle page
def riddle (username):
    return render_template("riddles.html")

@app.route("/leaderboard")
# route to leaderboard
def leaderboard():
    return render_template("leaderboard.html")
    
@app.route("/settings")
# route to settings page
def settings():
    return render_template("settings.html")

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=True)

 