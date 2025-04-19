import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=OPENAI_KEY)

def generate_commentary_script(title: str, description: str) -> str:
    prompt = f"""
        Generate a concise, engaging voiceover script for vertical Shorts video:

        Title: {title}
        Description: {description}

        Follow these rules exactly:
        1. Respond ONLY with the voiceover text. Do NOT include any commentary, explanations, or formatting markup.
        2. Use clear, simple language suitable for a broad audience.
        3. Avoid special characters or emojis (e.g., *, #, @, &, %, 🙂).
        4. Do not include profanity, slurs, or any NSFW content.
        5. Do NOT start with a greeting (e.g., "Hello," "Hey," etc.).
        6. Structure the script as:
        • Hook: 1–2 sentences to grab attention immediately.
        • Story: unfold the narrative or key points.
        • Payoff: 1–2 sentences delivering a satisfying conclusion.
        • Start with something like: "Did you know", or catchy line
    """

    openai_response = openai_client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return openai_response.output_text
