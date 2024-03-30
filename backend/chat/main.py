from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO
import redis 
import random 
import json
import string
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

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

def generate_unique_code():
    """
    Generate a unique room code that is 5 characters long and alphanumeric.

    :return: A unique room code.
    """
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        
        # Check if the room already exists in Redis
        metadata_key = f"room:{code}:metadata"
        if not redis_client.exists(metadata_key):
            break  # Unique code generated

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
            room = generate_unique_code(4)
            rooms[room] = {"members" : 0, "messages": []}

        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.")

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))
        

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    # Retrieve messages from Redis
    messages = r.lrange(f"room:{room}:messages", 0, -1)
    return render_template("room.html", code=room, messages=messages)

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):

    room = session.get("room") 
    if room not in rooms:
        return
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    # Store message in Redis
    r.rpush(f"room:{room}:messages", json.dumps(content))

    # send(content, room=room)

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect():

    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message" : "has entered the chat"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")




@socketio.on("disconnect")
def disconnect():

    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1 #counting the number of people in the room, this is not important for proj
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)

