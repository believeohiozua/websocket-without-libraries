import boto3
import base64
import time
from sender import send_message

def fetch_batch(folder, batch_num):
    '''Fetch batch from S3'''
    s3 = boto3.client( "s3", region_name='eu-west-1' )
    with open('batch.bt', 'wb') as data:
        s3.download_fileobj(
            "holotch-service-content", 
            f'archive/{folder}/{batch_num}.bt',
            data
            )
        data.close()

    '''Read downloaded binary file'''
    with open('batch.bt', 'rb') as file:   
        raw_data= file.read()
        '''Convert base64 data to binary data (buffer)'''
        to_binary = base64.b64decode(raw_data)
        file.close()
        return to_binary




def decoder(to_binary, batch_no): 
    
    total_size = len(to_binary) # --buffer size  
    '''Header information'''
    size = int.from_bytes(to_binary[:1], byteorder='big' , signed=True)
    size2 = int.from_bytes(to_binary[1:2], byteorder='big' , signed=True)
    byte3 = int.from_bytes(to_binary[2:3], byteorder='big' , signed=True)
    byte4 = int.from_bytes(to_binary[3:4], byteorder='big' , signed=True)        
    mesh_frame_size= int.from_bytes(to_binary[4:8], byteorder='little' , signed=True)
    timestamp = int.from_bytes(to_binary[8:12], byteorder='little' , signed=True)
    num_meshes = int.from_bytes(to_binary[12:16], byteorder='little', signed=True)
    valid_frame=[size,size2, byte3, byte4]

   
    if  valid_frame == [3,20,1,0]: #check if header is correct      
        frame_size=0
        frame_count = 0
        initial_mesh_frame_size=mesh_frame_size
        mesh_size_helper=0
        while total_size >= frame_size:                
            slice_frame = int.from_bytes(to_binary[frame_size:mesh_frame_size], byteorder='little', signed=True)
            frame = to_binary[frame_size:mesh_frame_size+slice_frame]
            
            '''convert binary to base64 encoded string'''
            frame_base64 = base64.b64encode(frame)
            frame_base64 = frame_base64.decode('utf-8')            
            frame_size=mesh_frame_size+4        
            mesh_frame_size=mesh_frame_size+8
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

            print(
                f'''
                \nbatch_no: {batch_no}
                \nmesh_frame_size{mesh_frame_size}
                \ntotal_size {total_size}
                \nframe_count {frame_count}
                \nframe_size: {frame_size}
                \n\n''')

            time.sleep(0.5)
            send_message(context)

        '''Start recursion to next batch'''
        batch_no += 1
        decoder(fetch_batch('hiroki1', batch_no), batch_no)

    else:
        '''Start recursion to next batch'''
        batch_no += 1
        decoder(fetch_batch('hiroki1', batch_no), batch_no)
