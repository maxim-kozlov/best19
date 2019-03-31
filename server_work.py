import socket
import json
import struct


# Courier between us and server
class Courier:

    def __init__(self):

        SERVER = "besthack19.sytes.net"
        TEAM = "11wake4pneo17io"

        self.sign = json.dumps({"team": TEAM, "task": 1})
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER, 4242))
        self.send_data(self.sign)
        self.first_bytes = 4

    # get server's answer
    def get_next_json(self) -> json:
        # Read len_of_data
        data_len = self.get_bytes(4)


        # decode data_len
        data_len = struct.unpack('<L', data_len)[0]

        # read the data
        data = self.get_bytes(data_len)

        # decode data
        data = data.decode()

        # make and return json
        a = json.loads(data)
        return a

    # get data
    def get_bytes(self, n) -> bytes or None:

        data = b''
        while len(data) < n:
            if n - len(data) <= 4096:
                packet = self.sock.recv(n - len(data))
            else:
                packet = self.sock.recv(4096)

            data += packet

        return data

    # send not encoded data(raw(not bytes))
    def send_data(self, message: (not bytes)):
        len_of_message = self.len_of_data(message)
        self.sock.send(len_of_message + message.encode())
        # print("Message send", len_of_message + message.encode())

    # get len in bytes
    def len_of_data(self, data):
        # print(struct.pack("<L", len(data)))
        return struct.pack("<L", len(data))

if __name__ == "__main__":
    server = Courier()
    a = server.get_next_json()
    print(a["map"])
