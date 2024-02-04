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
from adafruit_pm25.uart import PM25_UART

uart = busio.UART(board.GP8, board.GP9, baudrate=9600)
pm25 = PM25_UART(uart)

wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'),os.getenv('CIRCUITPY_WIFI_PASSWORD'))
print("Connect to Wifi")

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool, "/static")

def webpage(pm25_value,pm10_value,pm100_value):
    pm25_value_str = str(pm25_value)
    pm10_value_str = str(pm10_value)
    pm100_value_str = str(pm100_value)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>


    // Reload the page every 10 seconds
    setInterval(function() {{
        location.reload();
    }}, 10000);

    </script>
    <style>
      h1 {{
        text-align: center;
      }}

    </style>
    </head>
    <body>
    <h1>AQI Quality Monitor</h1>
    <center><b>
    <h1>PM2.5 : {pm25_value_str}</h1>
    <h2>PM10  : {pm10_value_str}</h2>
    <h2>PM100 : {pm100_value_str}</h2>
    
    <table width="380" >
      <tr bgcolor="#CCCCCC">
        <th>Index</th>
        <th>PM2.5</th>
        <th>PM10</th>
      </tr>
      <tr bgcolor="#00CCFF">
        <td align="center">0-25</td>
        <td align="center">0-15.5</td>
        <td align="center">0-50</td>
      </tr>
      <tr bgcolor="#00CC00">
        <td align="center">26-50</td>
        <td align="center">15.1-25.0</td>
        <td align="center">51-80</td>
      </tr>
      <tr bgcolor="#FFFF00">
        <td align="center">51-100</td>
        <td align="center">25.1-37.5</td>
        <td align="center">81-120</td>
      </tr>
      <tr bgcolor="#FFCC00">
        <td align="center">101-200</td>
        <td align="center">37.6-75.0</td>
        <td align="center">121-180</td>
      </tr>
      <tr bgcolor="#CC0000">
        <td align="center">>201</td>
        <td align="center">>75.1</td>
        <td align="center">>181</td>
      </tr>
    </table>
    
    </body></html>
    """
    return html

@server.route("/")
def base(request: HTTPRequest):  
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        try:
            aqdata = pm25.read()
            webpage_content = webpage(
                aqdata["pm25 standard"],
                aqdata["pm10 standard"],
                aqdata["pm100 standard"]
            )
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

    