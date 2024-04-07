import json 

def read_transcripts(filename):
    with open(filename  , 'r') as f:
        data = json.load(f)
    return data