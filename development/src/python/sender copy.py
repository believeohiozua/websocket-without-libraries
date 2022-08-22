from boto3.session import Session
import boto3
from decouple import config
from websocket import create_connection
import time
import json
import base64

import websockets
import asyncio
import json
import time

def fetch_batch(folder,batch_num):
    s3 = boto3.client(
        "s3", 
        # aws_access_key_id=config("ACCESS_KEY", cast=str, default=None),
        # aws_secret_access_key=config("SECRET_KEY", cast=str, default=None),
        region_name='eu-west-1'

        )
    with open('batch.bt', 'wb') as data:
        s3.download_fileobj("holotch-service-content", f'archive/{folder}/{batch_num}.bt', data)
    with open('batch.bt', 'r') as file:
   
        turn= file.read()
        to_base64 = base64.b64encode(turn.encode()).decode() #base64.b64encode(bytes(turn, "utf-8"))
        to_binary= base64.b64decode(to_base64)
        #get first 4 bytes of to_binary
        first_four = to_binary[:4]
        #get last 4 bytes of to_binary
        last_four = to_binary[-4:]
        #get the size of the byte array
        size = len(first_four)
        size2 = len(last_four)
        
        decoded = ""#base64.decodebytes(encoded)
        print(f"\n \n {type(to_base64)} \n {type(last_four)}\n {type(turn)} \n {size} \n{first_four}\n")
        return turn.split('//')
fetch_batch('hiroki1',1)
'''
#Start websocket transmission

async def listen():
    url = "ws://0.0.0.0:8000"
    async with websockets.connect(url) as ws:
        count = 1
        for msg in fetch_batch('hiroki1',1):
            count+=1
            data = {
                "command": "new_frame", 
                "sender": "py script", 
                "frame": msg, 
                "frameId": count, 
                "keyFrameID": count, 
            }
            time.sleep(0.5)
            await ws.send(json.dumps(data))

        while True:
            msg = await ws.recv()
            print(msg)


asyncio.get_event_loop().run_until_complete(listen())
# asyncio.get_event_loop().run_forever()

'''

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
'''
convert to binary from base64

base64 to byte
first 4 byte is header
next 4 byte
read all 4 byte and convert to int32 = size of frame 


4 bit header 
===================================================

def run(*args):
        count = 1
        for msg in fetch_batch('hiroki1',1):
            count+=1
            data = {
                "command": "new_frame", 
                "sender": "py script", 
                "frame": msg, 
                "frameId": count, 
                "keyFrameID": count, 
            }
            time.sleep(0.5)            
            ws.send(json.dumps(data)) 

def on_message(ws, message):
    print("message: ", message)
    

def on_error(ws, error):
    print("error: ", error)
    

def on_close(ws, message, error):
    print(f"closed: {message} {error}")

def on_open(ws):
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://0.0.0.0:8000",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close
                              )
    ws.on_open = on_open
    ws.run_forever()




    print(self.data)
    if self.data.get('command') == 'archive_id':
        decoder(fetch_batch(self.data.get('archive_id'),1),1)
        print(f'streaming archive: {self.data.get("archive_id")}')
    '''