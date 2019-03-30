import socket
HOST = "besthack19.sytes.net"
PORT = 4242
COMMAND = "11wake4pneo17io"


class we:

    def __init__(self, host=HOST, port=PORT, command=COMMAND):
        import socket

        self.host = host
        self.port = port
        self.command = command
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def __getBytes(self, string: str) -> bytes:
        return (len(string)).to_bytes(4, byteorder='little')

    def __createRequest(self, **kwargs) -> bytes:
        import json
        return self.__getBytes(str(kwargs)) + json.dumps(kwargs).encode()

    def takeText(self, string, parts=("{", "}")):
        return string[string.index(parts[0]) + 1: string.index(parts[1])]


    def __del__(self):
        self.sock.close()

    def __str__(self):
        print(f"""
            HOST: {self.host}
            PORT: {self.port}
            COMMAND: {self.command}
            SOCKET: {self.sock}
            """)

    def getData(self, debug=False, **kwargs) -> str:
        message = ""

        data = self.__createRequest(**kwargs)
        self.sock.send(data)

        while True:
            data = self.sock.recv(4096)
            
            if debug:
                print(data.decode())

            message += data.decode()

            if message.endswith("}"):
                break

        return message

    def parce(self, message, sep = '>'):
        """ Cleans data from unnessasary things """

        firstBrace = message.index("{")
        message = message[firstBrace:]

        message1, message2 = message.split(sep)

        return self.takeText(message1), self.takeText(message2)
