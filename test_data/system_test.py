import requests
import json

#TODO: fix the requests issue. getting BadStatusLine exceptions when curl seems
# to work fine

print("health check")
r0 = requests.post("https://localhost:8080/check", data = {})
print("response is ".format(r0.json()))

# create user1
print("creating test user 1")
data1 = {
    "username": "test1",
    "password" : "pw1"
}
r1 = requests.post("http://localhost:8080/createUser", data = data1)
print("response is ".format(r1.json()))

# create user2
print("creating test user 2")


# login user1 get token1
print("logging user 1 in")


# login user2 get token2
print("logging user 2 in")

# send messages from user1 to user2
print("sending 3 messages from user 1 to user 2")

# retrieve messages
print("retrieving all messages for user 2")

print("retrieving subset of messages for user 2")