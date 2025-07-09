import os
from openai import OpenAI

class OpenAIService:
    """
    This class is used to generate audio and captions with OpenAI
    """
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def generate_commentary_script(self, title: str, description: str) -> str:
        """
        Generate a concise, engaging voiceover script for vertical Shorts video
        """
        prompt = f"""
            Generate a concise, engaging voiceover script for vertical Shorts video:

            Title: {title}
            Description: {description}

            If you see that the content does not make sense, try to make a story out of it,
            but ONLY if it does not make sense at all. Othervise stick to original content story line.

            Follow these rules exactly:
            1. Respond ONLY with the voiceover text. Do NOT include any commentary, explanations, or formatting markup.
            2. Use clear, simple language suitable for a broad audience.
            3. Avoid special characters or emojis.
            4. Do not include profanity, slurs, or any NSFW content.
            5. Do NOT start with a greeting.
            6. Structure the script as:
            • Hook: 1–2 sentences to grab attention immediately.
            • Story: unfold the narrative or key points.
            • Payoff: 1–2 sentences delivering a satisfying conclusion.
            • Start with something like: "Did you know", or catchy line

            Make sure that the text is not too long and not too short. The video is from 15 to 20 seconds. Make sure the captions do not exceed the video duration.
        """
        try:
            # Generate commentary script using OpenAI
            openai_response = self.openai_client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            return openai_response.output_text
        except Exception as e:
            print(f"Error generating commentary script: {e}")
            raise e

    def text_to_speech_file(self, text: str, voice: str = "onyx") -> bytes:
        """
        Generate speech using OpenAI TTS API and return raw bytes.
        """
        try:
            # Generate speech using OpenAI TTS API
            response = self.openai_client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                speed=3,
                response_format='wav',
                input=text,
                instructions="Speak in a insightful and excited tone."
            )
            return response.content
        except Exception as e:
            print(f"Error generating speech: {e}")
            raise e
