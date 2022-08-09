from boto3.session import Session
import boto3
from decouple import config
from websocket import create_connection
import time
import json
import re
import ast


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
    with open('batch.txt', 'wb') as data:
        s3.download_fileobj("holotch-service-content", f'archive/{folder}/{batch_num}.bt', data)
    with open('batch.txt', 'r') as file:
   
        turn= file.read()
        return turn.split('//')


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
