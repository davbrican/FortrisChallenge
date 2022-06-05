from datetime import datetime
from distutils.log import debug
import random
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from flask_cors.core import try_match
from flask_mysqldb import MySQL
import os
import sys

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

try:
    app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
    app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
    app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
    app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
except:
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'RPSchallenge'


mysql = MySQL(app)


def gameLogic(username, machine_scores, user_scores, user_choice, game_round):
    choices = ["rock", "paper", "scissors"]
    machine_choice = random.choice(choices)
    
    result = ""
    if machine_choice == user_choice:
        machine_scores += 1
        user_scores += 1
        result = "There is a draw in the round"
    else:
        if machine_choice == "rock":
            if user_choice == "paper":
                machine_scores += 1
                result = "Computer wins!"
            else:
                user_scores += 1
                result = username + " win!"
        
        elif machine_choice == "paper":
            if user_choice == "scissors":
                machine_scores += 1
                result = "Computer wins!"
            else:
                user_scores += 1
                result = username + " win!"
        
        elif machine_choice == "scissors":
            if user_choice == "rock":
                machine_scores += 1
                result = "Computer wins!"
            else:
                user_scores += 1
                result = username + " win!"
    
    game_round += 1
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username LIKE %s", (username,))
    user_data = cur.fetchone()
    print(user_data, file=sys.stderr)
    if (machine_scores == 5):
        result = "Computer wins the game!"
        machine_scores = 0
        user_scores = 0
        game_round = 1
        cur.execute('UPDATE users SET scores = %s, matches = %s WHERE username LIKE %s', (user_data[2], user_data[3] + 1, username))
    elif (user_scores == 5):
        result = username + " win the game!"
        machine_scores = 0
        user_scores = 0
        game_round = 1
        cur.execute('UPDATE users SET scores = %s, matches = %s WHERE username LIKE %s', (user_data[2] + 3, user_data[3] + 1, username))
    mysql.connection.commit()
    
    return {"result": result, "machine_scores": machine_scores, "user_scores": user_scores, "game_round": game_round, "machine_choice": machine_choice}


#Testing Route
@app.route('/', methods=['GET'])
def getDefault():
    return jsonify({'response': 'Hello to my Rock-Paper-Scissors api!'})


#Get Users Routes
@app.route('/users')
def getUsers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    result = []
    for i in data:
        user = {
            "username": i[0],
            "password": i[1],
            "scores": i[2],
            "matches": i[3]
            }
        result.append(user)
        
    return jsonify(result)


#Get User By Username Routes
@app.route('/users/<string:username>')
def getUser(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username LIKE %s", (username,))
    if (len(cur.fetchall()) > 0):
        result = cur.fetchall()[0]
        result = {"username": result[0], "password": result[1], "scores": result[2], "matches": result[3]}

        return jsonify(result)
    
    return jsonify({"response": "There is no user with that username"})


#Get User By Username Routes
@app.route('/leaderboard')
def getLeaderboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ORDER BY scores DESC LIMIT 3")
    data = cur.fetchall()
    result = []
    for i in data:
        user = {
            "username": i[0],
            "password": i[1],
            "scores": i[2],
            "matches": i[3]
            }
        result.append(user)
        
    return jsonify(result)


# Sign Up Routes
@app.route('/signup', methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    repit_password = request.json['repit_password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username LIKE %s", (username,))
    data = cur.fetchall()
    if len(data) == 0:
        if (password == repit_password):
            cur.execute('INSERT INTO users (username, password, scores, matches) VALUES (%s, %s, %s, %s)', (username, password, 0, 0))
            mysql.connection.commit() 
            return jsonify({"response": "User created successfully"})
    
        return jsonify({"response": "Passwords do not match"})
    
    return jsonify({"response": "User already exists"})


# Login Routes
@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username LIKE %s", (username,))
    result = cur.fetchall()[0]
    if (result[1] == password):
        return jsonify({"username": result[0], "password": result[1], "scores": result[2], "matches": result[3], "response": "Login successful"}) 
    
    return jsonify({"response": "Invalid username or password"})


#Get Users Routes
@app.route('/game', methods=['POST'])
def game():
    username = request.json['username']
    machine_scores = request.json['machine_scores']
    user_scores = request.json['user_scores']
    user_choice = request.json['user_choice']
    game_round = request.json['game_round']
    
    return jsonify(gameLogic(username, machine_scores, user_scores, user_choice, game_round))


if __name__ == '__main__':
    app.run(debug=True)