import os
import asyncio, json
from moviepy.editor import *
from dotenv import load_dotenv
import logging, verboselogs
from datetime import datetime
import httpx
import multiprocessing

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)


logging.basicConfig(filename = 'out.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def main(filename: str) -> None:
    os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
    if not os.path.exists('transcripts'):
        os.makedirs('transcripts')

    audio_path = filename.replace('.mp4', '.mp3')
    if not _is_audio_file(audio_path):
        _extract_audio_from_video(filename, audio_path)
    
    transcription = _transcribe_audio_from_deepgram(audio_path)
    
    _save_transcription_to_file(transcription, filename="transcripts/"+filename.split('/')[-1].replace('.mp4', '.json'))

def _transcribe_audio_from_deepgram(audio_path) -> dict:
    try:
        config: DeepgramClientOptions = DeepgramClientOptions(
            verbose=logging.INFO,
        )
        deepgram: DeepgramClient = DeepgramClient("")
        
        with open(audio_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options: PrerecordedOptions = PrerecordedOptions(
            model="whisper-large",
            smart_format=True,
            punctuate=True,
        )

        before = datetime.now()
        response = deepgram.listen.prerecorded.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        after = datetime.now()
        logger.info(f"Transcription completed for {audio_path} Time: {after - before}")
        return response.to_dict()
    except Exception as e:
        print(f"Exception: {e}")

def _save_transcription_to_file(transcription, filename) -> None:
    with open (filename, 'w') as f:
        json.dump(transcription, f)

def _is_audio_file(filename) -> bool:
    if os.path.isfile(filename):
        return True
    return False

def _extract_audio_from_video(video_filename, audio_filename) -> None:
    video = VideoFileClip(video_filename)
    audio = video.audio
    audio.write_audiofile(audio_filename)

if __name__ == '__main__':  
    load_dotenv()
    PREFIXES = []
    for video in os.listdir('downloads'):
        if video.endswith('.mp4'):
            if video.replace('.mp4', '.json') in os.listdir('transcripts'):
                continue
            else:
                PREFIXES.append('downloads/'+video)
    logger.info(f"Number of videos to transcribe: {len(PREFIXES)}")
    # run the main function in parallel
    # with multiprocessing.Pool(processes=5) as pool:
    #     pool.map(main, PREFIXES)