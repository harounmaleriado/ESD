#!/usr/bin/env python3
from main.amqp_connection import create_connection
import json
import pika
from main.models.profile_models import db, Profile
#from os import environ


a_queue_name = 'Profile' # queue to be subscribed by Activity_Log microservice

# Instead of hardcoding the values, we can also get them from the environ as shown below
# a_queue_name = environ.get('Activity_Log') #Activity_Log

def receiveProfileData(channel, callback):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('Consuming from queue:', a_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("Program interrupted by user.") 


def createProfile(user):
    print("Creating profile data")
    print(user)
    user_id = user['user_id']
    #create a random placeholder name for the user
    name = "User" + str(user_id)
    profile = Profile(user_id=user_id, name=name, email=user['email'])
    Profile.create(profile)
    print("Profile created successfully")


def start_message_receiver(app):
    def callback(channel, method, properties, body): # required signature for the callback; no return
        print("\nReceived from: " + __file__)
        with app.app_context():
            createProfile(json.loads(body))
        print()
    print("Profile creation service: Getting Connection")
    connection = create_connection()  # get the connection to the broker
    print("Profile creation service: Connection established successfully")
    channel = connection.channel()
    receiveProfileData(channel, callback)
