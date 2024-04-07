from abc import ABC, abstractmethod

class BaseExtractor:
    def __init__(self):
        pass

    @abstractmethod
    def extract(self, filename, extraction_source):
        if extraction_source == "transcript":
            return self._extract_data_from_transcript(filename)
        elif extraction_source == "video":
            return self._extract_data_from_video(filename)
        elif extraction_source == "audio":
            return self._extract_data_from_audio(filename)
        else:
            raise ValueError("Invalid extraction source")
    
    @abstractmethod
    def _extract_data_from_transcript(self, transcript_filename):
        pass
    
    @abstractmethod
    def _extract_data_from_video(self, video_filename):
        pass
    
    @abstractmethod
    def _extract_data_from_audio(self, audio_filename):
        pass
    