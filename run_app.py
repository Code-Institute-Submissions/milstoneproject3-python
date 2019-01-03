import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
"""route to homepage """
def index():
    return render_template("index.html")
    
@app.route("/<username>")
"""route to userpage"""
def user(username):
    return "This is a page for:" + username

@app.route("/<username>/riddles")
"""route to riddle page"""
def riddle (username):
    return render_template("riddles.html")

@app.route("/leaderboard")
"""route to leaderboard"""
def leaderboard():
    return render_template("leaderboard.html")
    
@app.route("/settings")
"""route to settings page"""
def settings():
    return render_template("settings.html")

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=True)

 