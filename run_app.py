import os
import json
import random
from flask import Flask, render_template,request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = ("this is super secret")

# global variable to hold leaderboard
leader_list = [{"user":"USERNAME", "correct":"1", "incorrect":"2"},{"user":"ANOTHERUSER", "correct":"10", "incorrect":"20"}]


"""
Fucntion to check of a users answer is correct or incorrect and update the leader board on the fly.
"""
def checkAnswer(user_anwser, system_answer, username, leader_list):
    if "username" in session:
        if user_anwser.lower() in str(system_answer.lower()):
            session["correct"] += 1
        else:
            session["incorrect"] += 1
            
    add_to_leaderboard(username, session["correct"], session["incorrect"], leader_list)
    
    return "Correct: {} - Incorrect: {} for session user {}".format(session["correct"], session["incorrect"], username)

"""
functions that add and remove records from the leaderboard.  
NOTE: We are printing out various items to the app console as a visual means of keeping track of what is happening on the back end.
"""

# add/remove to leader board
def add_to_leaderboard(user, correct, incorrect, leader_list):
    
    check_pair = ("user", user)
    print("Check Pair = {}".format(check_pair))
    
    # check and delete user if already on board
    leader_list = remove_from_board(leader_list,check_pair) 
    
    leader_list.append({"user": user, "correct":correct, "incorrect":incorrect})

    num=0
    while num < len(leader_list):
        # print out currect leaderboard to web console.
        print(leader_list[num])
        num += 1
    
# remove key from leaderboard
def remove_from_board(leader_list, key):
    num = 0
    print("Check Cycle - {}".format(num))
    
    while num < len(leader_list): 
        # iterate through json and if we find a match for the user name, remove the entire entry for that user.
        list_of_pairs = leader_list[num].items()

        for item in list_of_pairs:
            print("ITEM to check against: {}".format(item))
            if key == item:
                print("Found KEY {} for removal from leaderboard data".format(key))
                leader_list.pop(num)
                break
        num += 1
        print("Check Cycle - {}".format(num))
        
    return leader_list

"""
Routes to pages
"""
@app.route("/", methods=["GET","POST"])
#  route to homepage
def index():
    if request.method =="POST":
        session["username"] = request.form["username"]
        username = session["username"]
        
    if "username" in session:
        session["correct"] = 0
        session["incorrect"] = 0
        print("New user login: {}".format(username))
        return redirect(url_for("riddles"))
    else:
        return render_template("index.html", page_title="Welcome to Riddles")

@app.route("/riddles", methods = ["GET","POST"])
# displayed riddle page with riddle data
def riddles ():
    riddles_dict=[]
    user_anwser = []
    score = ""
    board = leader_list
    
    #load data and select a random riddle to display to the user
    with open("data/riddles.json","r") as json_data:
        riddles_dict = json.load(json_data)
        select_riddle = random.choice(riddles_dict)
        system_answer = select_riddle["answer"]
    
    # checking for correct/incorrect answers    
    if request.method == "POST":
        user_anwser = request.form["user_input"]
        system_answer = select_riddle["answer"]
        username = session["username"]
        
        print("Check answer values - Username: '{}' UserAnswer: '{}' SystemAnswer: '{}'").format(username,user_anwser,system_answer)
        
        score = checkAnswer(user_anwser,system_answer, username, leader_list)
        
    return render_template("riddles.html", page_title ="Here are your riddles", data = select_riddle, score = score, username=session["username"], system_answer = system_answer)

@app.route("/leaderboard")
# route to leaderboard
def leaderboard():
    return render_template("leaderboard.html", page_title="Riddles Leaderboard", leader_list=leader_list)
    
@app.route("/settings")
# route to settings page
def settings():
    return render_template("settings.html", page_title="Riddles Settings")

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=True)

 