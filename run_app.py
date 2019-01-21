import os, json, time
from random import randint
from flask import Flask, render_template,request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = ("this is super secret")

# variables
leader_list = [{"user":"Joe Blogs", "correct":"0", "incorrect":"0"}]
user_sessions = []
random_riddle = []

"""
Fucntion to check of a users answer is correct or incorrect and update the leader board on the fly.
"""
def checkAnswer(user_anwser, system_answer, username, leader_list):
    print("UserAnswer: {} - SystemAnswer: {}".format(user_anwser, system_answer ))

    if user_anwser.lower() == system_answer.lower():
        session["correct"] += 1
    else:
        session["incorrect"] += 1
            
    add_to_leaderboard(username, session["correct"], session["incorrect"], leader_list)

    return "{}, you're current score is Correct: {} - Incorrect: {}".format(username, session["correct"], session["incorrect"])

"""
functions that add and remove records from the leaderboard.  
NOTE: We are printing out various items to the app console as a visual means of keeping track of what is happening on the back end.
"""

# add/remove to leader board
def add_to_leaderboard(user, correct, incorrect, leader_list):
    
    check_pair = ("user", user)
    
    # check and delete user if already on board
    leader_list = remove_from_board(leader_list,check_pair) 
    
    leader_list.append({"user": user, "correct": correct, "incorrect": incorrect})
    
# remove key from leaderboard
def remove_from_board(leader_list, key):
    num = 0
    
    while num < len(leader_list): 
        # iterate through json and if we find a match for the user name, remove the entire entry for that user.
        list_of_pairs = leader_list[num].items()

        for item in list_of_pairs:
            if key == item:
                leader_list.pop(num)
                break
        num += 1
        
    return leader_list

"""
Get a random riddle from the json file
"""

def get_riddle():
    
    #load data and select a random riddle to display to the user
    with open("data/riddles.json","r") as json_data:
        data = json.load(json_data)
        
    riddle_int = randint(0, len(data)) # get random riddle and answer for file
    return data[riddle_int]
        
"""
text input, checking for nulls
"""

def input_text(text_to_check, user):
    if not text_to_check:
        return True
    else:
        return False
        
"""
Detect duplicate users
"""

def duplicate_users(user_sessions):
    # we are iterating over all user session usernames added to user_sessions global variable, and looking multiples instances of the same name being used.  Returns True if we find one
    i = 0
    while i < len(user_sessions):
        count = 0
        n = 0
        while n < len(user_sessions):
            if user_sessions[i].lower() == user_sessions[n].lower():
                count += 1
                if count == 2:
                    user_sessions.remove(user_sessions[n])
                    return True
            n += 1
        i += 1

"""
Routes to pages
"""
@app.route("/", methods=["GET","POST"])
#  route to homepage
def index():
    if request.method =="POST":
        session["username"] = request.form.get("username","")#.encode('utf-8', 'ignore').decode('utf-8')
        username = session["username"]
        session["correct"] = 0
        session["incorrect"] = 0
        if input_text(username, username) == True:
            flash('You need to enter a user name')
            return redirect(url_for("index"))
        user_sessions.append(username)
        if duplicate_users(user_sessions) == True:
            flash('A user with this name is already logged in')
            return redirect(url_for("index"))
        
        return redirect(url_for("riddles"))
    
    return render_template("index.html", page_title="Welcome to Riddles")

@app.route("/riddles", methods = ["GET","POST"])
# displayed riddle page with riddle data
def riddles ():
    user_anwser = []
    score = ""
    
    if request.method =="POST":
        user_anwser = request.form.get("user_input", "").replace(" ", "")
        
        global random_riddle
        answer_to_check = random_riddle["answer"].replace(" ", "")
        
        username = session["username"]
        
        score = checkAnswer(user_anwser,answer_to_check, username, leader_list)
        
        return redirect(url_for("riddles"))
    
    random_riddle = get_riddle()
    print("Generate new riddle {}".format(random_riddle))
    return render_template("riddles.html", page_title="Here are your riddles",  score = score, username=session["username"], SelectRiddle = random_riddle["riddle"], systemAnswer = random_riddle["answer"])

@app.route("/leaderboard")
# route to leaderboard
def leaderboard():
    return render_template("leaderboard.html", page_title="Riddles Leaderboard", leader_list=leader_list)

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=False)