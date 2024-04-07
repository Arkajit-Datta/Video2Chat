import ast
import os 

from video2chat.llms.openai import OpenAILLM
from video2chat.utils.save_file import write_json
from video2chat.utils.response_cleaner import response_cleaner
from video2chat.process_data.utils.read_transcripts import read_transcripts
from video2chat.process_data.base_extractor import BaseExtractor

openai = OpenAILLM()


COOKING_STEPS_EXTRACTOR_PROMPT = """
You are a cooking video analyser. Your skills includes to read the transcription of the cooking video and extract the cooking steps from it.
Your job is given as follows - 
1. Analyse the transcription of the cooking video.
2. Extract the cooking steps from the transcription.
3. Always respond in the json format given below. 

Transcription: 
{transcription}

JSON Response:
{{
    "reasoning": "Give the detailed reasoning of the cooking steps you extracted from the transcription",
    "dish_description": "Brief description of the dish being cooked",
    "cooking_steps": [
        {{
            "step_number": 1,
            "description": "Give the detailed description of the first step here.",
        }},
        {{
            "step_number": 2,
            "description": "Give the detailed description of the second step here.",
        }},
        {{
            "step_number": 3,
            "description": "Give the detailed description of the third step here.",
        }},
        {{
            "step_number": 4,
            "description": "Give the detailed description of the fourth step here.",
        }},
        {{
            "step_number": 5,
            "description": "Give the detailed description of the fifth step here.",
        }},
        {{
            "step_number": 6,
            "description": "Give the detailed description of the sixth step here.",
        }},
        {{
            "step_number": 7,
            "description": "Give the detailed description of the seventh step here.",
        }},
        {{
            "step_number": 8,
            "description": "Give the detailed description of the eight step here.",
        }},
    ]
}}
"""

TIME_EXTRACTOR_PROMPT = """
You are given the transcription of the cooking video. You will also be provided with a description of a step in the cooking process.
Analysing the transcription where you are provided with the text and the time at which the text was spoken, you need to find the time at which the step was spoken.
Analyse all the time and text data and find the time at which the step was spoken.

INSTRUCTIONS:
1. Read the transcription of the cooking video.
2. The time should only be returned as an integer.
3. Remember to always respond in the json format given below.

Transcription:
{transcription}

Step Description:
{step_description}

JSON Response:
{{
    "start_time": "The time at which the step was spoken in the video",
    "end_time": "The time at which the step was completed in the video"
}}
"""

class CookingVideoExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
    
    def _extract_data_from_transcript(self, transcript_filename):
        try:
            transcript = self._format_transcription(transcript_filename)
            prompt = COOKING_STEPS_EXTRACTOR_PROMPT.format(transcription=transcript)
            
            print(prompt)
            
            response = openai.chat_completion(messages=[{"role": "user", "content": prompt}])
            
            response = response_cleaner(response)
            
            response_obj =  ast.literal_eval(response)
            
            for step in response_obj["cooking_steps"]:
                step_description = step["description"]
                time = self._extract_time_for_cooking_step(transcript, step_description)
                step["start_time"] = time["start_time"]
                step["end_time"] = time["end_time"]
            
            os.mkdir(f"processed_data/{transcript_filename.split('/')[-1].replace(".json", "")}")
            write_json(response_obj, f"processed_data/{transcript_filename.split('/')[-1].replace(".json", "")}/cooking_steps_extracted.json")
            return response_obj
        except Exception as e:
            print(f"Error in response: {e}")
            return None
    
    def _extract_time_for_cooking_step(self, transcript, step_description):
        prompt = TIME_EXTRACTOR_PROMPT.format(transcription=transcript, step_description=step_description)
        response = openai.chat_completion(messages=[{"role": "user", "content": prompt}])
        response = response_cleaner(response)
        print(f"step_description: {step_description} \n response: {response}")
        try:
            response_obj =  ast.literal_eval(response)
            return response_obj 
        except Exception as e:
            print(f"Error in response: {e}")
            
    def _extract_data_from_video(self, video_filename):
        pass
    
    def _extract_data_from_audio(self, audio_filename):
        pass
    
    
    def _format_transcription(self, transcript_filename) -> str:
        data = read_transcripts(transcript_filename)
        paragraphs = data["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
        
        transcript = ""
        for paragraph in paragraphs:
            for sentence in paragraph["sentences"]:
                transcript += f"TEXT: {sentence['text']}  < START: {int(float(sentence['start']))} secs  END: {int(float(sentence['end']))} secs > \n"
        return transcript
        