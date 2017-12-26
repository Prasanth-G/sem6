from http import server
import re

rc = re.compile(r'^/user=(.+?)&passwd=(.+)$')
user_cred = {  "hello" : "1234",
                "prasanth" : "6666",
                "pk" : "7777"}

class handler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        usrpass = rc.findall(self.path)
        if usrpass and len(usrpass[0]) == 2 :
            if self.valid_user(usrpass[0][0], usrpass[0][1]):
                self.send_response(200)
                self.end_headers()
                self.wfile.write("<h1>Login Success</h1>".encode())
            else:
                self.send_response(401)
                self.end_headers()

    def valid_user(self, username, password):
        if username in user_cred and password == user_cred[username]:
            return True
        return False

s = server.HTTPServer(('', 9000), handler)
print("Server Up")
s.serve_forever()