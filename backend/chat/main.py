from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
import redis 
import random 
import json
import string
from datetime import datetime

from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "shit"
socketio = SocketIO(app)

r = redis.Redis(
  host='redis-16378.c1.ap-southeast-1-1.ec2.cloud.redislabs.com',
  port=16378,
  password='muitCdS1YYaNGK1xUoCyouHthRJvjDnY')


redis_client = redis.StrictRedis(host='redis-16378.c1.ap-southeast-1-1.ec2.cloud.redislabs.com', port=16378, password='muitCdS1YYaNGK1xUoCyouHthRJvjDnY',  decode_responses=True)

try:
    response = redis_client.ping()
    if response:
        print("Connected to Redis successfully!")
    else:
        print("Failed to connect to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Redis connection error: {e}")

# rooms = {}

# def generate_unique_code(length):
#     while True:
#         code = ""
#         for _ in range(length):
#             code += random.choice(ascii_uppercase)

#         if code not in rooms:
#             break

#     return code

def generate_unique_code():
    """
    Generate a unique room code that is 5 characters long and alphanumeric.

    :return: A unique room code.
    """
    
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))        
    return code



@app.route('/test-redis')
def test_redis():
    # Try setting a value in Redis
    redis_client.set('test_key', 'Hello, Redis!')

    # Try retrieving the value
    value = redis_client.get('test_key')

    if value == 'Hello, Redis!':
        return 'Success! Connected to Redis and retrieved value: ' + value
    else:
        return 'Failed to connect to Redis or retrieve value.'

@app.route("/", methods =["POST","GET"])
def home():

    
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.")
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room.")
        
        room = code 
        if create != False:
            room = generate_unique_code()
            # rooms[room] = {"members" : 0, "messages": []}

        # elif code not in rooms:
        #     return render_template("home.html", error="Room does not exist.")

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))
        

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None :
        return redirect(url_for("home"))

  
    # return render_template("room.html", code=room, messages=messages)
     # Retrieve messages from Redis
    messages = r.lrange(f"room:{room}:messages", 0, -1)
    # Deserialize the JSON strings into dictionaries
    messages = [json.loads(message) for message in messages]
    # return render_template("room.html", code=room, messages=rooms[room]["messages"])
    return render_template("room.html", code=room, messages=messages)

@socketio.on("message")
def message(data):

    room = session.get("room") 
    
    
    # Get the current date and time
    now = datetime.now()
    # Format the date and time as a string, e.g., "2023-03-29 14:20:00"
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    content = {
        "name": session.get("name"),
        "message": data["data"],
        "timestamp": timestamp  # Add the timestamp to the content
    }

    # Store message in Redis, including the timestamp
    r.rpush(f"room:{room}:messages", json.dumps(content))
    # send(content, room=room)

    send(content, to=room)
    # rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect():

    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    # if room not in rooms:
    #     leave_room(room)
    #     return
    
    
    join_room(room)
    send({"name": name, "message" : "has entered the chat", "timestamp": " "}, to=room)
    # rooms[room]["members"] += 1
    print(f"{name} joined room {room}")




@socketio.on("disconnect")
def disconnect():

    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    
    send({"name": name, "message": "has left the room", "timestamp":" "}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)

