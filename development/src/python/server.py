from simple_websocket_server import WebSocketServer, WebSocket
import json

class SocketServer(WebSocket):
    def handle(self):
        for client in clients:
            if client != self:
                client.send_message(json.dumps(self.data))

    def connected(self):
        print(self.address, 'connected')
        for client in clients:
            if self.data:
                client.send_message(self.data)
        clients.append(self)

    def handle_close(self):
        clients.remove(self)
        print(self.address, 'left')

clients = []
port = 8000
server = WebSocketServer('', port, SocketServer)
print(f'server started at port {port}')
server.serve_forever()