import os
from openai import OpenAI
from io import BytesIO

openai_client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def generate_commentary_script(title: str, description: str) -> str:
    prompt = f"""
        Generate a concise, engaging voiceover script for vertical Shorts video:

        Title: {title}
        Description: {description}

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

        Make sure that the text is not too long and not too short. The video is from 15 to 30 seconds.
    """
    print('generating commentary script with openai api')
    openai_response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    print('done on commentary script with openai api')
    return openai_response.output_text

def text_to_speech_file(text: str, voice: str = "onyx") -> bytes:
    try:
        # Generate speech using OpenAI TTS API
        response = openai_client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            response_format='wav',
            input=text,
            instructions="Speak in a insightful and excited tone."
        )

        return response.content
    except Exception as e:
        print(f"Error generating speech: {e}")
        raise e
