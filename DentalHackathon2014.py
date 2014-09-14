import time
import BaseHTTPServer
import subprocess
from subprocess import call
import os
import shutil
import Image
import ImageFont
import ImageDraw 
import argparse
from Tkinter import Label, Button, Tk,Toplevel, Entry
import cgi

HOST_NAME       = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER     = 9000 # Maybe set this to 9000.
ALLOW_ALL       = False
APPROVED_USERS  = []

class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Approved user names separated by a comma\nEmpty to allow all.").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)
        self.APPROVED_USERS = []
        self.ALLOW_ALL = False

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()
        self.APPROVED_USERS = [x.strip().lower() for x in self.e.get().split(',') if len(x.strip())>0]
        if len(self.APPROVED_USERS)==0:
        	self.ALLOW_ALL=True
        print 'APPROVED_USERS', self.APPROVED_USERS
        print 'ALLOW_ALL', self.ALLOW_ALL

        self.top.destroy()




class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def greeting(self):
        self.wfile.write("""
<Response>
    <Say>Hello Patrick.</Say>
    <Say>The path is %s.</Say>
    <Play>http://demo.twilio.com/hellomonkey/monkey.mp3</Play>
    <Gather numDigits="1" action="hello-monkey-handle-key.php" method="POST">
        <Say>To speak to a real monkey, press 1.  Press any other key to start over.</Say>
    </Gather>
</Response>"""%(self.path))
    	
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.greeting()
        
        
        
    def do_POST(self):
        """Respond to a POST request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        if self.path=="/": self.greeting()
        
if __name__ == '__main__':
    import argparse

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)