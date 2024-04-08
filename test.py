import os
import multiprocessing

from video2chat.process_data.extractors.cooking_video_extractor import CookingVideoExtractor


def cooking_video_extractor():
    cooking_video_extractor = CookingVideoExtractor()
    transcripts_list = []
    for transcript in os.listdir('transcripts'):
        if transcript.endswith('.json') and transcript.replace(".json", "") not in os.listdir('processed_data'):
            transcripts_list.append(('transcripts/'+transcript, "transcript"))

    print(len(transcripts_list))
    with multiprocessing.Pool(processes=5) as pool:
        extracted_data = pool.starmap(cooking_video_extractor.extract, transcripts_list)
    print(extracted_data)
    
if __name__ == "__main__":
    cooking_video_extractor()
    