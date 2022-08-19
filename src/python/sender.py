from decoder import decoder, fetch_batch
import json
import ssl
import websocket
import rel

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("ws://0.0.0.0:8000")
to_binary = fetch_batch('hiroki1',1)
data= decoder(to_binary)
ws.send(json.dumps(data))
print(f'data sent!')
# result =  ws.recv()
'''end streaming manually with CTRL+C'''
rel.signal(2, rel.abort) 
rel.dispatch()
