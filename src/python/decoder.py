import boto3
import base64
import time


def fetch_batch(folder,batch_num):
    s3 = boto3.client( "s3", region_name='eu-west-1' )
    with open('batch.bt', 'wb') as data:
        s3.download_fileobj("holotch-service-content", f'archive/{folder}/{batch_num}.bt', data) #hiroki1/1.bt
        data.close()
    with open('batch.bt', 'rb') as file:   
        raw_data= file.read()
        '''Convert base64 data to binary data (buffer)'''
        to_binary = base64.b64decode(raw_data)
        file.close()
        return to_binary

      
    
            
fetch_batch('hiroki1',2)



def decoder(to_binary):    
    size = int.from_bytes(to_binary[:1], byteorder='big' , signed=True)
    size2 = int.from_bytes(to_binary[1:2], byteorder='big' , signed=True)
    byte3 = int.from_bytes(to_binary[2:3], byteorder='big' , signed=True)
    byte4 = int.from_bytes(to_binary[3:4], byteorder='big' , signed=True)        
    mesh_frame_size= int.from_bytes(to_binary[4:8], byteorder='little' , signed=True)
    timestamp = int.from_bytes(to_binary[8:12], byteorder='little' , signed=True)
    num_meshes = int.from_bytes(to_binary[12:16], byteorder='little', signed=True)
    valid_frame=[size,size2, byte3, byte4]
    if  valid_frame == [3,20,1,0]:
        ''' if false skip to the next batch'''
        frame_size=0
        frame_count = 0
        while True:   
            try:                 
                slice_frame = int.from_bytes(to_binary[frame_size:mesh_frame_size+frame_count], byteorder='little', signed=True)
                frame = to_binary[:slice_frame] 
                ''' convert binary to base64 encoded string '''
                frame_base64 = base64.b64encode(frame)
                frame_base64 = frame_base64.decode('utf-8')
                frame_size=mesh_frame_size
                frame_count += 1
                
                context =  {
                        "command": "new_frame", 
                        "sender": "js script", 
                        "frame": frame_base64,
                        "frameId": frame_count, 
                        "keyFrameID": frame_count, 
                    }

                meta_data = {
                    "timestamp":timestamp,
                    "num_meshes":num_meshes,
                    "frame":frame_base64,
                    "mesh_frame_size":mesh_frame_size
                    }

                time.sleep(0.5) 
                return context
            except Exception as e:
                print(e)
                break
    else:
        print('Header is incorrect')
        return None
