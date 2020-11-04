
import threading
import socket
import sys

############################################################################

HOST = ''    # Symbolic name, meaning all available interfaces
PORT = 8912  # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

############################################################################


def start_new_thread(f, args):

    threading.Thread(target=f, args=args).start()


def main():

    # Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    # Start listening on socket
    s.listen(10)

    print("Server listening on port " + str(PORT))

    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        sock, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        start_new_thread(clientHandler, (sock, addr[0]))

    s.close()

############################################################################


def clientHandler(sock, ip):

    # Sending message to connected client
    sock.send(b'You are now connected to the evil bunny trojan server')

    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        data = sock.recv(1024).decode('utf-8')

        print("[ %s ] %s" % (ip, data))
        reply = 'Received : ' + data
        sock.send(bytes(reply.encode('utf-8')))

        if not data:
            break

    # came out of loop
    sock.close()

############################################################################


main()
