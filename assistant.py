# assistant.py

import json
import random
import datetime

# Some starter advice snippets (expand these later)
TIPS = [
    "Drink some water and stand up for a bit!",
    "Small steps lead to big progress. Just start.",
    "Your future self will thank you for pushing through.",
    "Don't forget: breaks are productive, too.",
    "What you do today matters more than you think."
]

# Lambda entry point
def lambda_handler(event, context):
    # Get query param (ex: ?q=how are you)
    query = event.get("queryStringParameters", {}).get("q", "").strip().lower()

    # Very basic intent logic
    if not query:
        msg = "Hey! You didn’t say anything. Ask me something like 'how’s my day?' 😊"
    elif "day" in query or "mood" in query:
        now = datetime.datetime.now()
        msg = f"It’s {now.strftime('%A')} — a perfect day to make progress! 🌞"
    elif "help" in query or "advice" in query:
        msg = random.choice(TIPS)
    elif "who" in query:
        msg = "I'm your cloud-based coach, assistant, hype man, and loyal sounding board. 💼💬"
    else:
        msg = f"Hmm, I’m not sure how to respond to '{query}' yet... but I’m learning! 📚"

    response = {
        "message": msg,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }
