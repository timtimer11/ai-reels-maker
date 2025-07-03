from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions
from deepgram_captions import DeepgramConverter, srt
import os
import subprocess

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

class DeepgramService:
    """
    This class is used to generate audio and captions with Deepgram.
    """
    def __init__(self):
        self.deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)
        self.options = SpeakOptions(model='aura-orion-en',encoding='linear16')

    def generate_audio_with_deepgram(self, input_text: str) -> bytes:
        """
        Generate audio with Deepgram and return raw bytes.
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
            
            # Collect all chunks into a single bytes object
            chunks = []
            for data in response.iter_bytes():
                chunks.append(data)
            response.close()
            
            audio_bytes = b"".join(chunks)
            return audio_bytes

        except Exception as e:
            print(f"Error generating speech: {e}")
            raise

    def generate_captions_with_deepgram(self, audio_file_path: str) -> str:
        """
        Generate captions with Deepgram from an audio file path.
        """
        try:
            # Configure transcription options
            options = PrerecordedOptions(
                smart_format=True,
                model="nova-3",
                utterances=True,
                punctuate=True
            )

            with open(audio_file_path, "rb") as audio:
                source = {
                    "buffer": audio.read(),
                    "mimetype": "audio/wav"
                }
                response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(
                    source,
                    options
                )
            transcription = DeepgramConverter(response)
            return srt(transcription)

        except Exception as e:
            print(f"Error generating captions: {e}")
            raise

    def convert_srt_to_ass(self, srt_captions: str, srt_file_path: str, ass_file_path: str) -> None:
        """
        Convert SRT captions to ASS format using provided file paths.
        """
        try:
            # Write SRT content to provided path
            with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt_captions)

            # Convert using ffmpeg
            subprocess.run([
                "ffmpeg", "-y",
                "-i", srt_file_path,
                "-c:s", "ass",
                ass_file_path
            ], check=True, capture_output=True, text=True)

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg conversion failed: {e}")
            print(f"FFmpeg stdout: {e.stdout}")
            print(f"FFmpeg stderr: {e.stderr}")
            raise ValueError(f"FFmpeg failed to convert SRT to ASS: {e.stderr}") from e
        except Exception as e:
            print(f"Error converting SRT to ASS: {e}")
            raise
