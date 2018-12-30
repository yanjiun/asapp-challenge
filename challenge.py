#!/usr/bin/env python3

import contextlib
import http.server
import json
import sqlite3


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/check":
            self.handle_check()
    
    def handle_check(self):
        if self.query_health() != 1:
            raise Exception('unexpected query result')
        self.wfile.write(json.dumps({"health": "ok"}).encode('UTF-8'))
        self.send_response(200)

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
