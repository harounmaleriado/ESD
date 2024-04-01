import json
import math
import random
import redis
import bcrypt




SERVER_ID = random.uniform(0, 322321)

redis_client = redis.StrictRedis(host='redis-16378.c1.ap-southeast-1-1.ec2.cloud.redislabs.com', port=16378, password='muitCdS1YYaNGK1xUoCyouHthRJvjDnY',  decode_responses=True)


def get_messages(room_id=0, offset=0, size=50):
    """Check if room with id exists; fetch messages limited by size"""
    room_key = f"room:{room_id}"
    room_exists = redis_client.exists(room_key)
    if not room_exists:
        return []
    else:
        values = redis_client.zrevrange(room_key, offset, offset + size)
        return list(map(lambda x: json.loads(x.decode("utf-8")), values))


def hmget(key, key2):
    """Wrapper around hmget to unpack bytes from hmget"""
    result = redis_client.hmget(key, key2)
    return list(map(lambda x: x.decode("utf-8"), result))


def get_private_room_id(user1, user2):
    if math.isnan(user1) or math.isnan(user2) or user1 == user2:
        return None
    min_user_id = user2 if user1 > user2 else user1
    max_user_id = user1 if user1 > user2 else user2
    return f"{min_user_id}:{max_user_id}"


def create_private_room(user1, user2):
    """Create a private room and add users to it"""
    room_id = get_private_room_id(user1, user2)
    if not room_id:
        return None, True

    # Add rooms to those users
    redis_client.sadd(f"user:{user1}:rooms", room_id)
    redis_client.sadd(f"user:{user2}:rooms", room_id)

    return (
        {
            "id": room_id,
            "names": [
                hmget(f"user:{user1}", "username"),
                hmget(f"user:{user2}", "username"),
            ],
        },
        False,
    )


def init_redis():
    # We store a counter for the total users and increment it on each register
    total_users_exist = redis_client.exists("total_users")
    if not total_users_exist:
        # This counter is used for the id
        redis_client.set("total_users", 0)
        # Some rooms have pre-defined names. When the clients attempts to fetch a room, an additional lookup
        # is handled to resolve the name.
        # Rooms with private messages don't have a name
        redis_client.set(f"room:0:name", "General")

        # demo_data.create()

# We use event stream for pub sub. A client connects to the stream endpoint and listens for the messages


def event_stream():
    """Handle message formatting, etc."""
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("MESSAGES")
    for message in pubsub.listen():
        message_parsed = json.loads(message["data"])
        if message_parsed["serverId"] == SERVER_ID:
            continue

        data = "data:  %s\n\n" % json.dumps(
            {"type": message_parsed["type"], "data": message_parsed["data"],}
        )
        yield data

def add_message(room_id, from_id, content, timestamp):
    room_key = f"room:{room_id}"
    message = {
        "from": from_id,
        "date": timestamp,
        "message": content,
        "roomId": room_id,
    }
    # Now the other user sends the greeting to the user
    redis_client.zadd(room_key, {json.dumps(message): int(message["date"])})
