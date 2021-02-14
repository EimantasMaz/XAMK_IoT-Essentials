#################################################################
#                                                               #
#        XAMK IoT - Assignment3 - Home Security Cam             #
#                                                               #
#                                        Eimantas Mažeika 2021  #
#################################################################


#Based on: https://nostarch.com/RaspberryPiProject



import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

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
        <title>Raspberry Pi - Surveillance Camera</title>
        <script defer src="script.js"></script>
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">    </head>
    <body>
        <header>
            <h1>Raspberry Pi - Surveillance Camera</h1>
            <span class="author-name">By Eimantas Mažeika</span>
        </header>
        <div class="main">
            <img src="stream.mjpg" width="1280" height="720">
        </div>
    </body>
</html>
"""

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
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
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

with picamera.PiCamera(resolution='1280x720', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
