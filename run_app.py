import os
import json
import random
from flask import Flask, render_template,request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = ("this is super secret")


# function to check user answers and keep count of correct and incorrect answers
def checkAnswer(user_input, system_answer, session_user):
    if "username" in session:
        if user_input == system_answer:
            session["correct"] =+ 1
        else:
            session["incorrect"] += 1
    return "Correct: {} - Incorrect: {} for session user {}".format(session["correct"], session["incorrect"], session_user)

@app.route("/", methods=["GET","POST"])
#  route to homepage
def index():
    if request.method =="POST":
        session["username"] = request.form["username"]
        username = session["username"]
        
    if "username" in session:
        session["correct"] = 0
        session["incorrect"] = 0
        return redirect(url_for("riddles"))
    else:
        return render_template("index.html", page_title="Welcome to Riddles")

@app.route("/riddles", methods = ["GET","POST"])
# displayed riddle page with riddle data
def riddles ():
    riddles_dict=[]
    user_anwser = []
    score = ""
    
    #load data and select a random riddle to display to the user
    with open("data/riddles.json","r") as json_data:
        riddles_dict = json.load(json_data)
        select_riddle = random.choice(riddles_dict)
        system_answer = select_riddle["answer"]
    
    # checking for correct/incorrect answers    
    if request.method == "POST":
        user_anwser = request.form["user_input"]
        system_answer = select_riddle["answer"]

        score = checkAnswer(user_anwser, system_answer, session["username"])
        
    return render_template("riddles.html", page_title ="Here are your riddles", data = select_riddle, score = score, username=session["username"], system_answer = system_answer)

@app.route("/leaderboard")
# route to leaderboard
def leaderboard():
    return render_template("leaderboard.html", page_title="Riddles Leaderboard")
    
@app.route("/settings")
# route to settings page
def settings():
    return render_template("settings.html", page_title="Riddles Settings")

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=True)

 