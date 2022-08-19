from boto3.session import Session
import boto3
import base64
import sys

# print(f"\n\n\n{sys.byteorder}")

'''
4 bytes: header 3 20 0 0
int32: size of mesh frame (total number of bytes including the header)
int32: timestamp
int32: number of meshes
(This part times the number of meshes){
int64: source (individual id linked to the camera the mesh comes from)
int32: draco data size
draco data size × bytes : draco data
int32: ffmpeg data size
ffmpeg data size × bytes : ffmpeg data
'''


def fetch_batch(folder,batch_num):
    s3 = boto3.client(
        "s3", 
        region_name='eu-west-1'

        )
    with open('batch.bt', 'wb') as data:
        s3.download_fileobj("holotch-service-content", f'archive/{folder}/{batch_num}.bt', data) #hiroki1/1.bt
    with open('batch.bt', 'rb') as file:   
        raw_data= file.read()
        '''Convert base64 data to binary data (buffer)'''
        to_binary = base64.b64decode(raw_data)
        print(f"\n to binary{to_binary[:10]}")
        
        '''
        4 bytes: header 3 20 0 0
        int32: size of mesh frame (total number of bytes including the header)
        int32: timestamp
        int32: number of meshes

2.bt

        4 bytes: header 3 20 0 0
        int32: size of mesh frame (total number of bytes including the header)
        int32: timestamp
        int32: number of meshes
        '''
        # header = int.from_bytes(to_binary, byteorder="big", signed=True)
        # print(f'Header: {header}')
        # #check if header is correct
        # if header == 32000:
        #     print('Header is correct')
        # else:
        #     print('Header is incorrect')
        #get next 4 bytes of to_binary
        size = int.from_bytes(to_binary[:1], byteorder='big' , signed=True)
        size2 = int.from_bytes(to_binary[1:2], byteorder='big' , signed=True)
        byte3 = int.from_bytes(to_binary[2:3], byteorder='big' , signed=True)
        byte4 = int.from_bytes(to_binary[3:4], byteorder='big' , signed=True)
        
        mesh_frame_size= int.from_bytes(to_binary[4:8], byteorder='little' , signed=True)
        timestamp = int.from_bytes(to_binary[8:12], byteorder='little' , signed=True)
        num_meshes = int.from_bytes(to_binary[12:16], byteorder='little', signed=True)
        
        first_frame = to_binary[:mesh_frame_size]
        # print(first_frame)
        #convert binary to base64
        base64_data = base64.b64encode(first_frame)
        print(f"\n base64_data{base64_data}")
        next_header = int.from_bytes(to_binary[mesh_frame_size:mesh_frame_size+1], byteorder='little', signed=True)

        print(f'Size: {size}\n')
        print(f'Size2: {size2}\n')

        print(f'byte3: {byte3}\n')
        print(f'byte4: {byte4}\n')
        print(f'mesh_frame_size: {mesh_frame_size}\n')
        
        print(f'Timestamp: {timestamp}\n')
        print(f'Number of meshes: {num_meshes}\n')
        print(f'next_header: {next_header}\n')


        '''
        (This part times the number of meshes){
        int64: source (individual id linked to the camera the mesh comes from)
        int32: number of vertices
        double × 3 × number of vertices: vertices data
        int32: number of triangles
        int32 × 3 × number of triangles: triangles data
        int32: number of uvs
        double × 2 × number of uvs: uvs data
        int32: ffmpeg data size
        ffmpeg data size × bytes : ffmpeg data)
        '''

        # for i in range(num_meshes):
        #     #get next 8 bytes of to_binary
        #     source = int.from_bytes(to_binary[12+(i*24):16+(i*24)], byteorder='big')
        #     #get next 4 bytes of to_binary
        #     num_vertices = int.from_bytes(to_binary[16+(i*24):20+(i*24)], byteorder='big')
        #     #get next num_vertices*3 bytes of to_binary
        #     vertices = to_binary[20+(i*24):20+(i*24)+num_vertices*3]
        #     #get next 4 bytes of to_binary
        #     num_triangles = int.from_bytes(to_binary[20+(i*24)+num_vertices*3:24+(i*24)+num_vertices*3], byteorder='big')
        #     #get next num_triangles*3 bytes of to_binary
        #     triangles = to_binary[24+(i*24)+num_vertices*3:24+(i*24)+num_vertices*3+num_triangles*3]
        #     #get next 4 bytes of to_binary
        #     num_uvs = int.from_bytes(to_binary[24+(i*24)+num_vertices*3+num_triangles*3:28+(i*24)+num_vertices*3+num_triangles*3], byteorder='big')
        #     #get next num_uvs*2 bytes of to_binary
        #     uvs = to_binary[28+(i*24)+num_vertices*3+num_triangles*3:28+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2]
        #     #get next 4 bytes of to_binary
        #     ffmpeg_data_size = int.from_bytes(to_binary[28+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2:32+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2], byteorder='big')
        #     #get next ffmpeg_data_size bytes of to_binary
        #     ffmpeg_data = to_binary[32+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2:32+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2+ffmpeg_data_size]
        #     #get next 4 bytes of to_binary
        #     draco_data_size = int.from_bytes(to_binary[32+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2+ffmpeg_data_size:36+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2+ffmpeg_data_size], byteorder='big')
        #     #get next draco_data_size bytes of to_binary
        #     draco_data = to_binary[36+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2+ffmpeg_data_size:36+(i*24)+num_vertices*3+num_triangles*3+num_uvs*2+ffmpeg_data_size+draco_data_size]
        #     #get next 4 bytes of to_binary            


        #     print(f'Source: {source}\n')
        #     print(f'Number of vertices: {num_vertices}\n')
        #     print(f'Vertices: {vertices}\n')
        #     print(f'Number of triangles: {num_triangles}\n')


        #get next 4 bytes of to_binary
        # for i in range(num_meshes):
        #     #get next 8 bytes of to_binary
        #     source = int.from_bytes(to_binary[16+(i*16):24+(i*16)], byteorder='big')
        #     #get next 4 bytes of to_binary
        #     draco_size = int.from_bytes(to_binary[24+(i*16):28+(i*16)], byteorder='big')
        #     #get next draco_size bytes of to_binary
        #     draco_data = to_binary[28+(i*16):28+(i*16)+draco_size]
        #     #get next 4 bytes of to_binary
        #     ffmpeg_size = int.from_bytes(to_binary[28+(i*16)+draco_size:32+(i*16)+draco_size], byteorder='big')
        #     #get next ffmpeg_size bytes of to_binary
        #     ffmpeg_data = to_binary[32+(i*16)+draco_size:32+(i*16)+draco_size+ffmpeg_size]
        #     #print data
        #     print(f'Source: {source}')
        #     print(f'Draco data size: {draco_size}')
        #     print(f'Draco data: {draco_data}')
        #     print(f'Ffmpeg data size: {ffmpeg_size}')
        #     print(f'Ffmpeg data: {ffmpeg_data}')
        #     print('\n')
    
            
fetch_batch('hiroki1',2)