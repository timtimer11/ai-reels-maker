import os
from deepgram import DeepgramClient, SpeakOptions, PrerecordedOptions
from deepgram_captions import DeepgramConverter, srt

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

class DeepgramService:
    """
    This class is used to generate audio and captions with Deepgram
    """
    def __init__(self):
        self.deepgram_client = DeepgramClient(DEEPGRAM_API_KEY)
        self.audio_options = SpeakOptions(
            model='aura-2-apollo-en',
            encoding='linear16'
        )
        self.caption_options = PrerecordedOptions(
            smart_format=True,
            model="nova-3",
            utterances=True,
            punctuate=True
        )

    def generate_audio_with_deepgram(self, input_text: str) -> bytes:
        """
        Generate audio with Deepgram and return raw bytes
        """
        try:
            # Build request body using input text
            request_body = {
                "text": input_text
            }
            
            # Generate audio using Deepgram
            response = self.deepgram_client.speak.rest.v("1").stream_raw(
                request_body,
                self.audio_options
            )
            
            # Collect all chunks into a single bytes object
            chunks = []
            for data in response.iter_bytes():
                chunks.append(data)
            response.close()
            audio_bytes = b"".join(chunks)
            return audio_bytes

        except Exception as e:
            raise ValueError(f"Error generating speech: {e}") from e

    def generate_captions_with_deepgram(self, audio_file_path: str) -> str:
        """
        Generate captions with Deepgram from an audio file path
        """
        try:
            # Transcribe audio file using Deepgram
            with open(audio_file_path, "rb") as audio:
                source = {
                    "buffer": audio.read(),
                    "mimetype": "audio/wav"
                }
                response = self.deepgram_client.listen.prerecorded.v("1").transcribe_file(
                    source,
                    self.caption_options
                )
            # Process transcription response
            transcription = DeepgramConverter(response)
            return srt(transcription) # Return transcription in SRT format

        except Exception as e:
            raise ValueError(f"Error generating captions: {e}") from e
