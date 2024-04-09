import os
import multiprocessing

from video2chat.process_data.utils.read_transcripts import read_transcripts
from video2chat.memory.chromadb import ChromaDB
from video2chat.process_data.extractors.cooking_video_extractor import CookingVideoExtractor

    
def cooking_video_extractor():
    cooking_video_extractor = CookingVideoExtractor()
    transcripts_list = [
        (f'transcripts/{transcript}', "transcript")
        for transcript in os.listdir('transcripts')
        if transcript.endswith('.json')
        and transcript.replace(".json", "") not in os.listdir('processed_data')
    ]
    print(len(transcripts_list))
    with multiprocessing.Pool(processes=5) as pool:
        extracted_data = pool.starmap(cooking_video_extractor.extract, transcripts_list)
    print(extracted_data)

def build_cooking_vector_db():
    
    collection_name = "jacques_pepin_cooking"
    db = ChromaDB(collection_name=collection_name, embedding_model=None, text_field="dish_description")
    db.create_collection(collection_name)
    
    
    text_datas, metadatas = [], []
    for folder in os.listdir('processed_data'):
        name_of_video = folder 
        video_data = read_transcripts(f"processed_data/{folder}/cooking_steps_extracted.json")
        
        text_datas.append(f"{name_of_video}: {video_data['dish_description']}")
        metadatas.append({
            "path": f"processed_data/{folder}/cooking_steps_extracted.json" 
        })
    
    db.add_texts(text_datas, metadatas)


def query_cooking_vector_db(query):
    collection_name = "jacques_pepin_cooking"
    db = ChromaDB(collection_name=collection_name, embedding_model=None, text_field="dish_description")
    
    print(db.get_matching_text(query, top_k=10))

if __name__ == "__main__":
    # cooking_video_extractor()
    # build_cooking_vector_db()
    query_cooking_vector_db("How to make spinach?")
    