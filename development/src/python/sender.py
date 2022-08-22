import json
import ssl
import websocket
import rel

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("ws://0.0.0.0:8000")

def send_message(message):   
    ws.send(json.dumps(message))
    print('data sent!', end='')

def id_receiver():
    return 'hiroki1'

response = ws.recv()
print(response)

'''end streaming manually with CTRL+C'''
# rel.signal(2, rel.abort) 
# rel.dispatch()
