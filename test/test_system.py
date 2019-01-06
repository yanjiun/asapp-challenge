import requests
import json


def test_health():
    print("health check")
    r0 = requests.post("http://localhost:8080/check")
    assert(r0.status_code==200)

def create_user_success():
    # create user1
    print("creating test user 1")
    data1 = {
        "username": "test1",
        "password" : "pw1"
    }
    dataString = json.dumps(data1).encode('utf8')
    r1 = requests.post("http://localhost:8080/createUser", data = dataString)
    print("response is ".format(r1.json()))


def create_user_failure():
    print("create user but user already exists")
    data1 = {
        "username": "test1",
        "password" : "pw1"
    }
    dataString = json.dumps(data1).encode('utf8')
    r1 = requests.post("http://localhost:8080/createUser", data = dataString)
    assert(r1.status_code == 501)

# create user2
def create_user_success2():
    print("creating test user 2")
    data1 = {
        "username": "test2",
        "password" : "pw2"
    }
    dataString = json.dumps(data1).encode('utf8')
    r1 = requests.post("http://localhost:8080/createUser", data = dataString)
    print("response is ".format(r1.json()))

def login_user_1():
    # login user1 get token1
    print("logging user 1 in")

def login_user_2():
    # login user2 get token2
    print("logging user 2 in")

def send_messages(token):
    # send messages from user1 to user2
    print("sending 3 messages from user 1 to user 2")

def get_messages(token):
    # retrieve messages
    print("retrieving all messages for user 2")

def get_subset_messages():
    print("retrieving subset of messages for user 2")

def main():
    test_health()
    create_user_success()
    create_user_failure()
    create_user_success2()
    token1 = login_user_1()
    token2 = login_user_2()
    send_messages(token1)
    send_messages(token2)


if __name__ == '__main__':
    main()