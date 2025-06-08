from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions
from deepgram_captions import DeepgramConverter, srt
from dotenv import load_dotenv
import os
from io import BytesIO
import tempfile
import subprocess

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

class DeepgramService:
    def __init__(self):
        self.deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)
        self.options = SpeakOptions(model='aura-2-thalia-en')

    def generate_audio_with_deepgram(self, input_text: str) -> bytes:
        try:
            # Create the request body as shown in documentation
            request_body = {
                "text": input_text
            }
            
            response = self.deepgram_client.speak.rest.v("1").stream_raw(
                request_body,
                self.options
            )
            
            # Create a BytesIO object to store the audio data
            audio_data = BytesIO()
            
            # Write all bytes from the response to our BytesIO object
            for data in response.iter_bytes():
                audio_data.write(data)
                
            # Reset the pointer to the beginning of the BytesIO object
            audio_data.seek(0)
            
            # Close the response
            response.close()
            
            return audio_data
        except Exception as e:
            print(f"Error generating speech: {e}")
            raise e

    def generate_captions_with_deepgram(self, AUDIO_FILE: bytes) -> str:
        try:
            # Create a temporary file to store the audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
                # Write the audio bytes to the temporary file
                tmp.write(AUDIO_FILE)
                tmp.flush()
                
                # Configure transcription options
                options = PrerecordedOptions(
                    smart_format=True,
                    model="nova-3",
                    utterances=True,
                    punctuate=True
                )
                
                # Open the file and send it to Deepgram
                with open(tmp.name, "rb") as audio:
                    source = {
                        "buffer": audio.read(),
                        "mimetype": "audio/wav"
                    }
                    response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(
                        source,
                        options
                    )
                
                transcription = DeepgramConverter(response)
                srt_captions = srt(transcription)
                
                return srt_captions
                
        except Exception as e:
            print(f"Error generating captions: {e}")
            raise e

    def convert_srt_to_ass(self, srt_captions: str) -> str:
        try:
            # Create temporary files for SRT and ASS
            with tempfile.NamedTemporaryFile(delete=True, suffix=".srt") as srt_file, \
                 tempfile.NamedTemporaryFile(delete=True, suffix=".ass") as ass_file:
                
                # Write SRT content to temporary file
                srt_file.write(srt_captions.encode('utf-8'))
                srt_file.flush()
                
                # Convert using ffmpeg
                subprocess.run([
                    "ffmpeg", "-y",
                    "-i", srt_file.name,
                    "-c:s", "ass",
                    ass_file.name
                ], check=True)
                
                # Read the ASS content before the file is deleted
                with open(ass_file.name, "r", encoding="utf-8") as f:
                    ass_content = f.read()
                
                return ass_content
                    
        except Exception as e:
            print(f"Error converting SRT to ASS: {e}")
            raise e

# if __name__ == "__main__":
#     deepgram_service = DeepgramService()
#     audio_data = deepgram_service.generate_audio_with_deepgram("Hello, world! This is a test of the deepgram api.")
#     captions = deepgram_service.generate_captions_with_deepgram(audio_data.getvalue())
#     ass_captions = deepgram_service.convert_srt_to_ass(captions)
