#!/usr/bin/env python3

import contextlib
import http.server
import json
import sqlite3
import user_handlers
import sessions
import messages

class Handler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/check":
            self.handle_check()
        elif self.path == "/login":
            post_data = self._get_postdata()
            self.handle_login(post_data)
        elif self.path == "/createUser":
            post_data = self._get_postdata()
            self.handle_create_user(post_data)
        elif self.path == "/message":
            post_data = self._get_postdata()
            self.handle_send_message(post_data)

    def do_GET(self):
        if self.path == "/messages":
            post_data = self._get_postdata()
            self.handle_get_messages(post_data)

    def _get_postdata(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n"
              % (str(self.path), str(self.headers), post_data.decode('utf-8')))
        return post_data
    
    def handle_check(self):
        if self.query_health() != 1:
            raise Exception('unexpected query result')
        self.wfile.write(json.dumps({"health": "ok"}).encode('UTF-8'))
        self.send_response(200)

    def handle_login(self, postdata):
        request = json.loads(postdata)
        if (user_handlers.login_existence(self.server.conn, request["username"])):
            user_id, token = sessions.login_user(self.server.conn, request["username"], request["password"])
            self.wfile.write(json.dumps({"id": user_id, "token": token}).encode('UTF-8'))
            self.send_response(200)

    def handle_send_message(self, postdata):
        request = json.loads(postdata)
        print("header keys are ", self.headers.keys())
        token = self.headers.get("Authorization").strip("Bearer").strip()
        print("token is ", token)
        if sessions.authenticate(self.server.conn, request["sender"], token):
            message_id, timestamp = \
                messages.record_message(self.server.conn, request["sender"], request["receiver"], request["content"])
            response = {"id": message_id, "timestamp": timestamp}
            self.wfile.write(json.dumps(response).encode('UTF-8'))
            self.send_response(200)
        else:
            self.wfile.write(json.dumps({"error": "Authentication Error"}).encode('UTF-8'))
            self.send_response(401)

    def handle_create_user(self, postdata):
        request = json.loads(postdata)
        print("request is: ", request)
        try:
            user_id = user_handlers.create_user(self.server.conn, request["username"], request["password"])
            self.wfile.write(json.dumps({"id": user_id }).encode('UTF-8'))
            self.send_response(200)
        except user_handlers.UserAlreadyExists:
            self.wfile.write(json.dumps({"error": "username already exists"}).encode('UTF-8'))
            self.send_response(501)
        except:
            self.wfile.write(json.dumps({"error": "unknown error"}).encode('UTF-8'))
            self.send_response(500)

    def handle_get_messages(self, postdata):
        request = json.loads(postdata)
        print("header keys are ", self.headers.keys())
        token = self.headers.get("Authorization").strip("Bearer").strip()
        print("token is ", token)
        if sessions.authenticate(self.server.conn, request["recipient"], token):
            limit = 100 if not "limit" in request else request["limit"]
            msg_list = messages.get_messages(self.server.conn, request["recipient"], request["start"], limit)
            self.wfile.write(json.dumps(msg_list).encode('UTF-8'))
            self.send_response(200)
        else:
            self.wfile.write(json.dumps({"error": "Authentication Error"}).encode('UTF-8'))
            self.send_response(401)

    def query_health(self):
        with contextlib.closing(self.server.conn.cursor()) as cur:
            cur.execute('SELECT 1')
            (res, ) = cur.fetchone()
            return res


class Server(http.server.HTTPServer):
    def __init__(self, address, conn):
        super().__init__(address, Handler)
        self.conn = conn


def main():
    conn = sqlite3.connect('challenge.db')
    address = ('localhost', 8080)
    httpd = Server(address, conn)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
