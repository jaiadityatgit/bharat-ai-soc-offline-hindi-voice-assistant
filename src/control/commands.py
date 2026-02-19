# commands.py
# Maps Hindi spoken text → intent → response

from datetime import datetime

def recognize_intent(text):
    t = text.lower().strip()

    if any(w in t for w in ['समय','कितने बजे']):
        return "time"

    if any(w in t for w in ['तारीख','आज']):
        return "date"

    if any(w in t for w in ['तापमान','गरमी','ठंड']):
        return "temperature"

    if any(w in t for w in ['नमस्ते','hello','hi']):
        return "greet"

    if any(w in t for w in ['धन्यवाद','thanks']):
        return "thanks"

    if any(w in t for w in ['तुम कौन','नाम']):
        return "identity"

    if any(w in t for w in ['मदद','help']):
        return "help"

    if any(w in t for w in ['जोक']):
        return "joke"

    if any(w in t for w in ['तथ्य']):
        return "fact"

    if any(w in t for w in ['अलविदा','bye','बंद']):
        return "bye"

    return None


def get_response(intent):
    now = datetime.now()

    if intent == "time":
        return f"अभी {now.hour} बजकर {now.minute} मिनट है।"

    if intent == "date":
        return f"आज {now.day}-{now.month}-{now.year} है।"

    if intent == "temperature":
        return "तापमान सेंसर उपलब्ध नहीं है।"

    if intent == "greet":
        return "नमस्ते! मैं आपकी हिंदी सहायक हूँ।"

    if intent == "thanks":
        return "आपका स्वागत है।"

    if intent == "identity":
        return "मैं एक ऑफलाइन हिंदी वॉइस सहायक हूँ।"

    if intent == "help":
        return "आप समय, तारीख, तथ्य, या सवाल पूछ सकते हैं।"

    if intent == "joke":
        return "प्रोग्रामर चाय क्यों पीते हैं? क्योंकि कोड ठंडा हो जाता है।"

    if intent == "fact":
        return "भारत दुनिया का सबसे बड़ा लोकतंत्र है।"

    if intent == "bye":
        return "अलविदा! फिर मिलेंगे।"

    return "माफ़ करें, समझ नहीं आया।"
