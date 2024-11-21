import network
import socket
from time import sleep
import machine
from machine import Pin, PWM

# Yes, these could be in another file. But on the Pico! So no more secure. :)
ssid = 'Your WiFi'
password = 'Your WiFi password'

# Define pins to pin motors!
Mot_A_Forward = Pin(18, Pin.OUT)
Mot_A_Back = Pin(19, Pin.OUT)
Mot_B_Forward = Pin(20, Pin.OUT)
Mot_B_Back = Pin(21, Pin.OUT)

Mot_Speed = PWM(Pin(22))
Mot_Speed.freq(5000) # PWM frequency setting
Mot_Speed.duty_u16(32750) # Initial speed at approx 50% speed




def move_forward():
    Mot_A_Forward.value(1)
    Mot_B_Forward.value(1)
    Mot_A_Back.value(0)
    Mot_B_Back.value(0)
    
def move_backward():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(1)
    Mot_B_Back.value(1)

def move_stop():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(0)
    Mot_B_Back.value(0)

def move_left():
    Mot_A_Forward.value(1)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(0)
    Mot_B_Back.value(1)

def move_right():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(1)
    Mot_A_Back.value(1)
    Mot_B_Back.value(0)
    
    
def speed_change(speed):
    duty = speed * 655
    Mot_Speed.duty_u16(duty) # duty must be a number between 0 and 65536
   


# Stop the robot as soon as possible
move_stop()
    
def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    # Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Zumo Robot Control</title>
            </head>
            <center><b>
<h1>Vehicle Direction</h1>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
            
<h1>Vary Vehicle Speed</h1>
            <table><tr>
            <td><form action="./25">
            <input type="submit" value="25%" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./50">
            <input type="submit" value="50%" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./75">
            <input type="submit" value="75%" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./100">
            <input type="submit" value="100%" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
# direction control
        if request == '/forward?':
            move_forward()
        elif request =='/left?':
            move_left()
        elif request =='/stop?':
            move_stop()
        elif request =='/right?':
            move_right()
        elif request =='/back?':
            move_backward()
# speed control portion         
        elif request =='/25?':
            speed_change(25)
        elif request =='/50?':
            speed_change(50)    
        elif request =='/75?':
            speed_change(75)
        elif request =='/100?':
            speed_change(100)    
            
            
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

    