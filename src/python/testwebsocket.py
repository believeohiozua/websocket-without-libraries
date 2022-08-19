import ssl
import websocket
import rel
import json 

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("ws://0.0.0.0:5000")
ws.send(json.dumps({
        "command": "get_latest",
        "slug": "admin",
    }))
result =  ws.recv()
print("Received '%s'" % json.loads(result))

# ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
rel.signal(2, rel.abort)  # Keyboard Interrupt
rel.dispatch()
