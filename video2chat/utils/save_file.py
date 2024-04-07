import json 

def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)