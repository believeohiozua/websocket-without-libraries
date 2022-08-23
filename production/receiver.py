import json
import ssl
import websocket
from decouple import config
from decoder import decoder
import time

url=config("CONNECT_STRING", default="ws://176.34.6.114:80",  cast=str)

def receiver():
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(url)
    print('listening...')
    while True:
        msg = json.loads(ws.recv())
        print(msg)
        data = json.loads(msg)
        print(data['command'], data['archive_id'])
        if data['command'] == 'archive_id':
            decoder(data['archive_id'],1)

receiver()


