import requests
import json


def test_health(start_server):
    print("health check")
    r0 = requests.post("http://localhost:8080/check")
    response_data = json.loads(r0.json())
    assert(r0.status_code==200)


def create_user_success(start_server):
    self.send_response(200)


# create user1
print("creating test user 1")
data1 = {
    "username": "test1",
    "password" : "pw1"
}
dataString = json.dumps(data1).encode('utf8')
r1 = requests.post("http://localhost:8080/createUser", data = dataString)
print("response is ".format(r1.json()))

print("create user but user already exists")
data1 = {
    "username": "test1",
    "password" : "pw1"
}
dataString = json.dumps(data1).encode('utf8')
r1 = requests.post("http://localhost:8080/createUser", data = dataString)
assert(r1.status_code == 501)

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