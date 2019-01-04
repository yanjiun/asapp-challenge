#!/usr/bin/env python3

import sqlite3
import sys


def create_db(name):
    conn = sqlite3.connect(name)
    c = conn.cursor()

    c.execute('''CREATE TABLE users
        (user_id integer PRIMARY KEY, 
        username text UNIQUE, 
        password text)''')

    c.execute('''CREATE TABLE sessions
        (user_id integer PRIMARY KEY,
         token   text    UNIQUE)''')

    c.execute('''CREATE TABLE messages
        (message_id integer, 
        sender_id integer, 
        receiver_id integer,
        metadata blob,
        timestamp text, 
        FOREIGN KEY (sender_id) REFERENCES users(user_id))''')

    conn.commit()

    conn.close()


if __name__ == "__main__":
    create_db(sys.argv[1])
