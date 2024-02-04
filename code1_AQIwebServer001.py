import os
import time
import ipaddress
import wifi
import socketpool
import board
import busio
import digitalio
from digitalio import DigitalInOut,Direction
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType

wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'),os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("Connect to Wifi")

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool, "/static")

def webpage():
    html="""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <h1>Welcome to Web Server By Yakroo108</h1>
    </body></html>
    """
    return html

@server.route("/")
def base(request: HTTPRequest):
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        try:
            webpage_content = webpage()
            response.send(f"{webpage_content}")
        except RuntimeError:
            response.send("Unable to read from sensor, retrying...")
print("Starting server..")
try :
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s" % wifi.radio.ipv4_address)
except OSError:
    time.sleep(5)
    print("Restarting..")
    microcontroller.reset()
    
while True:
    try:
        server.poll()
    except Exeception as e:
        print(e)
        continue

    