import os
import json
import random
from flask import Flask, render_template,request, session, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = ("this is super secret")

# global variables
leader_list = [{"user":"USERNAME", "correct":"1", "incorrect":"2"}]
user_sessions = []

"""
Fucntion to check of a users answer is correct or incorrect and update the leader board on the fly.
"""
def checkAnswer(user_anwser, system_answer, username, leader_list):
    print("PreCheck user answer: {}").format(user_anwser)
    print("PreCheck sysem answer: {}").format(system_answer)
    
    if user_anwser.lower() == system_answer.lower():
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
Get a random riddle from the json file
"""
def get_riddle(data):
    random_riddle = random.choice(data) # get random riddle and answer for file

    print("SelectRiddle on page load: {}").format(random_riddle["riddle"])
    print("SystemAnswer on page load: {}").format(random_riddle["answer"])
        
    return random_riddle
        

"""
text input, checking for nulls
"""

def input_text(text_to_check, user):
    if not text_to_check:
        print("The username is empty")
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
            if user_sessions[i] == user_sessions[n]:
                count += 1
                print(count)
                if count == 2:
                    print("Duplicate user found: {}".format(user_sessions[n]))
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
        session["username"] = request.form["username"]
        username = session["username"]
        
        global user_sessions
        user_sessions.append(username)
 
    if "username" in session:
        if input_text(username, username) == True:
            flash('You need to enter a user name')
            return render_template("index.html", page_title="Welcome to Riddles")
        elif duplicate_users(user_sessions) == True:
            flash('A user with this name is already logged in')
            return render_template("index.html", page_title="Welcome to Riddles")
        else:
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
    
    random_riddle = get_riddle(riddles_dict)
    
    # checking for correct/incorrect answers    
    if request.method == "POST":
        user_anwser = request.form["user_input"]
        answer_to_check = random_riddle["answer"]
        username = session["username"]
        
        print("Check answer values - Username: '{}' UserAnswer: '{}' AnswerToCheck: '{}'").format(username,user_anwser,answer_to_check)
        
        score = checkAnswer(user_anwser,answer_to_check, username, leader_list)

    return render_template("riddles.html", page_title ="Here are your riddles", score = score, username=session["username"], SelectRiddle = random_riddle["riddle"], systemAnswer = random_riddle["answer"])

@app.route("/leaderboard")
# route to leaderboard
def leaderboard():
    return render_template("leaderboard.html", page_title="Riddles Leaderboard", leader_list=leader_list)

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT","5000")), debug=True)

 