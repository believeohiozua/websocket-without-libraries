from boto3.session import Session
import boto3
from decouple import config
from websocket import create_connection
import time
import json
import re
import ast

def fetch_batch(folder,batch_num):
    s3 = boto3.client(
        "s3", 
        # aws_access_key_id=config("ACCESS_KEY", cast=str, default=None),
        # aws_secret_access_key=config("SECRET_KEY", cast=str, default=None),
        region_name='eu-west-1'

        )
    with open(f'{batch_num}.txt', 'wb') as data:
        s3.download_fileobj("holotch-service-content", f'archive/{folder}/{batch_num}.bt', data)
    with open(f'{batch_num}.txt', 'r') as file:
   
        turn= file.read()
        return turn.split('//')

# print(fetch_batch('hiroki1',1))

ws = create_connection("ws://0.0.0.0:8000")
count= 1
for msg in fetch_batch('hiroki1',1):
    count+=1
    data = {
        "command": "new_frame", 
        "sender": "py script", 
        "frame": msg, 
        "frameId": f"{count}", 
        "keyFrameID": f"{count}", 
      }
    time.sleep(1)
    # d = json.loads(f"{data}")#.replace('\"', '')))#
    
    # p = re.compile('(?<!\\\\)\'')
    # e = p.sub('\"', json.dumps(data))
    parsed_json = ast.literal_eval(json.dumps(data))
    print(parsed_json)
    # send json data to server
    ws.send(json.dumps(parsed_json))
    # ws.send(parsed_json)
# result = ws.recv()
# print('Result: {}'.format(result))