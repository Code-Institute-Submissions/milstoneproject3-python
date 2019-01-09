import os
import json
import random
from flask import Flask, render_template,request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = ("this is super secret")

@app.route("/", methods=["GET","POST"])
#  route to homepage
def index():
    if request.method =="POST":
        session["username"] = request.form["username"]
        username=session["username"]
        
    if "username" in session:
        return redirect(url_for("riddles"))
    else:
        return render_template("index.html", page_title="Welcome to Riddles")

@app.route("/riddles", methods = ["GET","POST"])
# displayed riddle page with riddle data
def riddles ():
    riddles_dict=[]
    correct = 0
    incorrect = 0
    
    #load data
    with open("data/riddles.json","r") as json_data:
        riddles_dict = json.load(json_data)
    
    #checking for correct/incorrect answers    
    if request.method == "POST":
        user_anwser = request.form["answer"]
        if user_anwser == riddles_dict[request.form["index"]]["answer"]:
            correct =+ 1
            flash(user_anwser +" Right")
        else:
            incorrect =+ 1
            flash(user_anwser +" Wrong")
        
    
    return render_template("riddles.html", page_title ="Here are your riddles", data = riddles_dict, correct=correct, incorrect=incorrect, username=session["username"])

@app.route("/leaderboard")
# route to leaderboard
def leaderboard():
    return render_template("leaderboard.html", page_title="Riddles Leaderboard")
    
@app.route("/settings")
# route to settings page
def settings():
    return render_template("settings.html", page_title="Riddles Settings")

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=True)

 