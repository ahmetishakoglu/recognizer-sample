import snowboydecoder
import sys
import signal
import requests
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 6677
message = ""

# Demo code for listening two hotwords at the same time

interrupted = False

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def requests_open():
    message = "Open Light"
    r = requests.post('https://httpbin.org/post')
    print(r.text)
    print("Open")
    sock.sendto(message,(UDP_IP,UDP_PORT))

def requests_close():
    message = "Close Light"
    r = requests.get('https://httpbin.org/get')
    print(r.text)
    print("Close")
    sock.sendto(message,(UDP_IP,UDP_PORT))


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) != 3:
    print("Error: need to specify 2 model names")
    print("Usage: python demo.py 1st.model 2nd.model")
    sys.exit(-1)

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [requests_open, requests_close]

print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
