import socket
import time
import RPi.GPIO as GPIO
from http import server
import fcntl
import socketserver
from threading import Condition
from http import server
import picamera
import io
import logging
import struct

msgsocketserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
msgsocketserver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

BUTTON_PIN = 2                              # Set Button pin
GPIO.setmode(GPIO.BCM)		                # Use Broadcom SoC pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN)	            # Set pin as an input
ip = '192.168.1.4'
port = 8000


PAGE="""\
<html>
    <head>
        <style>
            html {
            margin: 0;
            padding: 0;
            font-family: 'Roboto', serif;
        }
        body {
            margin: 0;
            padding: 0;
            background-color: #004D40;
        }
        header {
            color: #FAFAFA;
            background-color: #263238;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: 0.25s;
            text-align: center;
            height: 10%;
            padding-top: 12px;
            box-shadow: 0 0 20px 1px black;
        }
        header:hover {
            transition: 0.25s;
            height: 25%;
        }
        header:hover .author-name {
            transform: scale(1);
            opacity: 1;
            transition: 0.25s;
        }
        .author-name {
            opacity: 0;
            transition: 0.25s;
            transform: scale(0);
        }
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        video {
            margin-top: 150px;
            box-shadow: 0 0 8px 1px black;
        }
        img {
            margin-top: 150px;
            box-shadow: 0 0 8px 1px black;
        }
        </style>
        <meta charset="UTF-8">
        <title>Raspberry Pi - IoT Doorbell Camera</title>
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">    </head>
    <body>
        <header>
            <h1>Raspberry Pi - IoT DoorBell Camera</h1>
            <span class="author-name">By Eimantas Mažeika</span>
        </header>
        <div class="main">
            <img src="stream.mjpg" width="1280" height="720">
        </div>
    </body>
</html>
"""

# Code from the Raspberry Pi security camera challenge:

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            #new frame, copy the existing buffer's content and notify all
            #clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with streamingoutput.condition:
                        streamingoutput.condition.wait()
                        frame = streamingoutput.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def start_stream():
    global streamingoutput

    with picamera.PiCamera(resolution='1280x720', framerate=24) as camera:
        streamingoutput = StreamingOutput()
        camera.start_recording(streamingoutput, format='mjpeg')
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()




def button_pressed_callback(channel):       # Function for Button Interrupt 
    print("[LOG] Button pressed!")
    msg = ip + ":" + str(port)
    message = msg.encode('UTF-8')
    msgsocketserver.sendto(message, ('<broadcast>', 37020))
    print("alert sent!")
    print("[LOG] Stream started. IP: ", ip)
    start_stream()


# Configure Interrupt:
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=100)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
msgsocketserver.settimeout(0.2)
msgsocketserver.bind(("", 44444))
message = b"your very important message"
while True: 
    # We don't need to do anything special
    # Button is configured with an
    time.sleep(1)

