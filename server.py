#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    @staticmethod
    def getResponse(route: str, http_method: str):
        # Check invalid http method 
        if http_method != "GET":
            return "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n"
        
        # Define the response content based on route
        if route.endswith(".css"):
            file_path = f"./www{route}"
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n"
        elif route.endswith("index.html"):
            file_path = f'./www{route}'
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        elif not route.endswith("/"):
            route += "/"
            # Have to redirect
            return f"HTTP/1.1 301 Moved Permanently\r\nLocation: {route}\r\nContent-Type: text/html\r\n\r\n"
        else: 
            file_path = f'./www{route}/index.html'
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

        # Check if file path exist
        if not os.path.exists(file_path):
            return "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        
        # Read the content of file and return
        with open(file_path, 'rb') as css_file:
            css_content = css_file.read()
        return header + css_content.decode('utf-8')
    
    @staticmethod
    def getRouteAndMethod(request_data):
        request_parts = request_data.decode('utf-8').split()
        return request_parts[1], request_parts[0]
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        url_path, http_method = MyWebServer.getRouteAndMethod(self.data)
        response = MyWebServer.getResponse(url_path, http_method)
        self.request.sendall(bytearray(response, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
