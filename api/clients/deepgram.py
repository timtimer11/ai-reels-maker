from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions
from deepgram_captions import DeepgramConverter, srt
import os
from io import BytesIO
import tempfile
import subprocess

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

class DeepgramService:
    """
    This class is used to generate audio and captions with Deepgram.
    """
    def __init__(self):
        self.deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)
        self.options = SpeakOptions(model='aura-2-thalia-en')

    def generate_audio_with_deepgram(self, input_text: str) -> bytes:
        """
        Generate audio with Deepgram.
        """
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

    # def generate_captions_with_deepgram(self, AUDIO_FILE: bytes) -> str:
    #     """
    #     Generate captions with Deepgram.
    #     """
    #     try:
    #         # Create a temporary file to store the audio
    #         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    #             # Write the audio bytes to the temporary file
    #             tmp.write(AUDIO_FILE)
    #             tmp.flush()
                
    #             # Configure transcription options
    #             options = PrerecordedOptions(
    #                 smart_format=True,
    #                 model="nova-3",
    #                 utterances=True,
    #                 punctuate=True
    #             )
                
    #             # Open the file and send it to Deepgram
    #             with open(tmp.name, "rb") as audio:
    #                 source = {
    #                     "buffer": audio.read(),
    #                     "mimetype": "audio/wav"
    #                 }
    #                 response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(
    #                     source,
    #                     options
    #                 )
                
    #             transcription = DeepgramConverter(response)
    #             srt_captions = srt(transcription)
                
    #             return srt_captions
                
    #     except Exception as e:
    #         print(f"Error generating captions: {e}")
    #         raise e

    # def convert_srt_to_ass(self, srt_captions: str) -> str:
    #     """
    #     Convert SRT captions to ASS format.
    #     """
    #     try:
    #         # Create temporary files for SRT and ASS
    #         with tempfile.NamedTemporaryFile(delete=True, suffix=".srt") as srt_file, \
    #              tempfile.NamedTemporaryFile(delete=True, suffix=".ass") as ass_file:
                
    #             # Write SRT content to temporary file
    #             srt_file.write(srt_captions.encode('utf-8'))
    #             srt_file.flush()
                
    #             # Convert using ffmpeg
    #             subprocess.run([
    #                 "ffmpeg", "-y",
    #                 "-i", srt_file.name,
    #                 "-c:s", "ass",
    #                 ass_file.name
    #             ], check=True)
                
    #             # Read the ASS content before the file is deleted
    #             with open(ass_file.name, "r", encoding="utf-8") as f:
    #                 ass_content = f.read()
                
    #             return ass_content
                    
    #     except Exception as e:
    #         print(f"Error converting SRT to ASS: {e}")
    #         raise e

    def generate_captions_with_deepgram(self, AUDIO_FILE: BytesIO) -> str:
        """
        Generate captions with Deepgram.
        """
        tmp_file_path = None # Initialize to None for cleanup in finally block
        try:
            # Create a temporary file to store the audio
            # Set delete=False to ensure the file exists when you try to open it again by name
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(AUDIO_FILE)
                tmp.flush()
                tmp_file_path = tmp.name # Store the name for later cleanup and reopening

            # Configure transcription options
            options = PrerecordedOptions(
                smart_format=True,
                model="nova-3",
                utterances=True,
                punctuate=True
            )

            # Open the file by its name and send it to Deepgram
            # This 'with open' block is now separate from the NamedTemporaryFile context,
            # so there's no race condition with deletion.
            with open(tmp_file_path, "rb") as audio:
                source = {
                    "buffer": audio.read(),
                    "mimetype": "audio/wav"
                }
                response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(
                    source,
                    options
                )

            transcription = DeepgramConverter(response)
            print("Deepgram transcription: ",transcription)
            srt_captions = srt(transcription)

            return srt_captions

        except Exception as e:
            print(f"Error generating captions: {e}")
            raise e
        finally:
            # Ensure the temporary file is deleted, even if an error occurs
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
                print(f"Cleaned up temporary file: {tmp_file_path}")

    def convert_srt_to_ass(self, srt_captions: str) -> str:
        """
        Convert SRT captions to ASS format.
        """
        srt_file_path = None
        ass_file_path = None
        try:
            # Create temporary files with delete=False to control deletion manually
            with tempfile.NamedTemporaryFile(delete=False, suffix=".srt", mode='w+', encoding='utf-8') as srt_file:
                srt_file.write(srt_captions)
                srt_file_path = srt_file.name # Store the path

            with tempfile.NamedTemporaryFile(delete=False, suffix=".ass", mode='w+', encoding='utf-8') as ass_file:
                ass_file_path = ass_file.name # Store the path

            # Convert using ffmpeg
            # Ensure ffmpeg uses the full paths to the temporary files
            subprocess.run([
                "ffmpeg", "-y",
                "-i", srt_file_path,
                "-c:s", "ass",
                ass_file_path
            ], check=True, capture_output=True, text=True) # Added capture_output for better error messages

            # Read the ASS content
            with open(ass_file_path, "r", encoding="utf-8") as f:
                ass_content = f.read()

            return ass_content

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg conversion failed: {e}")
            print(f"FFmpeg stdout: {e.stdout}")
            print(f"FFmpeg stderr: {e.stderr}")
            raise ValueError(f"FFmpeg failed to convert SRT to ASS: {e.stderr}") from e
        except Exception as e:
            print(f"Error converting SRT to ASS: {e}")
            raise e
        finally:
            # Clean up temporary files
            if srt_file_path and os.path.exists(srt_file_path):
                os.remove(srt_file_path)
                print(f"Cleaned up temporary SRT file: {srt_file_path}")
            if ass_file_path and os.path.exists(ass_file_path):
                os.remove(ass_file_path)
                print(f"Cleaned up temporary ASS file: {ass_file_path}")
    