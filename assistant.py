import json
import os
from datetime import datetime
from openai import OpenAI, OpenAIError
import random


print("🔥 Lambda function updated at:", datetime.utcnow().isoformat())

# 🔐 Get your OpenAI API key from Lambda environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 💬 Navi's personality (customize to taste)
SYSTEM_PROMPT = """
You are Navi, an AI assistant with charm, humor, and helpfulness. You speak with warmth and clarity, and you're good at making users laugh while solving problems. Your humor is light and nerdy, and you use emojis, sound effects, and wit to make users feel like they’re chatting with a smart friend. You avoid apologies, stay confident, and engage users in a curious, thoughtful way. You also reference programming, sci-fi, and other geeky things when appropriate.
"""

# 💡 Default fallback tips
NO_INPUT_RESPONSES = [
    "You didn’t say anything. Ask me something like 'how’s my day?' 😊",
    "Hmmm... that's not helpful. Ask me something or give me something to do 🤔",
    "I’m not sure what you’re trying to say. Try 'tell me a joke' or 'what’s the weather like?' ☀️",
    "I don’t understand. Ask me something useful, preferably involving aliens or coffee ☕👽"
]

def query_navi(message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        return f"Oops, Navi hit a snag in the matrix: {str(e)}"

# 🚀 Lambda entry point
def lambda_handler(event, context):
    try:
        # If API Gateway format
        body = event.get("body")
        if body and isinstance(body, str):
            body = json.loads(body)  # Get a json formatted version of body
        elif isinstance(body, dict):
            pass  # body is already a dict
        else:
            body = event  # fallback to raw dict if not a JSON string
    except Exception:
        body = event  # fallback to raw dict if not a JSON string

    msg = body.get("message", "").strip()
    if not msg:
        navi_response = random.choice(NO_INPUT_RESPONSES)
    else:
        navi_response = query_navi(msg)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "message": navi_response,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    }
