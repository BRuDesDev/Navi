# assistant.py

import json
import random
import datetime

# Some starter advice snippets (expand these later)
TIPS = [
    "Don't stare into the sun.",
    "Look both ways before crossing the street... Cockadoodledoo",
    "Small steps lead to big progress. Just start.",
    "Your future self will thank you for pushing through.",
    "Don't forget: breaks are productive, too.",
    "Stuck with errors flying about is how you learn."
]

NO_INPUT_WARN = [
    "Hey! You didn’t say anything. Ask me something like 'how’s my day?' 😊",
    "Hmmm... that's not helpful. Ask me something or give me something to do 😊",
    "I’m not sure what you’re trying to say. Ask me something like 'how’s my day?' 😊",
    "I don’t understand. Ask me something like 'how’s my day?' 😊"
]

# Lambda entry point
def lambda_handler(event, context):
    # Get query param (ex: ?q=how are you)
    query = event.get("queryStringParameters", {}).get("q", "").strip().lower()

    # Very basic intent logic
    if not query:
        # Randomly pick one of the strings from our list of warnings
        msg = random.choice(NO_INPUT_WARN)
    elif "day" in query or "mood" in query:
        now = datetime.datetime.now()
        msg = f"It’s {now.strftime('%A')} — a perfect day to make progress! 🌞"
    elif "help" in query or "advice" in query:
        msg = random.choice(TIPS)
    elif "who" in query:
        msg = "I'm your cloud-based coach, assistant, hype man, and loyal sounding board. 💼💬"
    else:
        msg = f"Hmm, I’m not sure how to respond to '{query}' yet... I'm still learning and my master has ADHD! 📚"

    response = {
        "message": msg,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }
