from decoder import decoder, fetch_batch
from sender import id_receiver

if __name__ == '__main__':
    '''Start decoding'''
    decoder(fetch_batch(id_receiver(),1),1)