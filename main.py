import json
import os
from dotenv import load_dotenv

# ✅ Correct import for new Gemini SDK
import google.genai as genai

# ---------------- LOAD ENV ----------------
load_dotenv()

# ✅ Secure API key usage
client = genai.Client(api_key=os.getenv("AIzaSyB2yVy8rdxtXbc3oe8nGwIFbzZlIkrMSHE"))

# ---------------- LOAD KNOWLEDGE BASE ----------------
def load_data():
    with open("knowledge_base.json") as f:
        return json.load(f)

data = load_data()

# ---------------- AI INTENT DETECTION ----------------
def detect_intent(user_input):
    prompt = f"""
    Classify the user intent into one of these:
    greeting, inquiry, high_intent

    Input: {user_input}
    Answer ONLY one word.
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    # ✅ Clean output
    return response.text.strip().lower().split()[0]

# ---------------- AI RESPONSE (RAG STYLE) ----------------
def answer_query(query):
    context = json.dumps(data)

    prompt = f"""
    You are AutoStream AI assistant.

    Use ONLY this data:
    {context}

    Answer clearly and professionally.

    User: {query}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text.strip()

# ---------------- MOCK TOOL ----------------
def mock_lead_capture(name, email, platform):
    print(f"\n✅ Lead captured successfully: {name}, {email}, {platform}\n")

# ---------------- STATE MEMORY ----------------
state = {
    "intent": None,
    "name": None,
    "email": None,
    "platform": None,
    "stage": "start"
}

# ---------------- MAIN LOOP ----------------
def run_agent():
    print("🤖 AutoStream AI Agent (Gemini Final Version) Started (type 'exit' to stop)\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break

        intent = detect_intent(user_input)
        state["intent"] = intent

        # -------- GREETING --------
        if intent == "greeting":
            print("Agent: Hello! How can I help you today?")

        # -------- INQUIRY --------
        elif intent == "inquiry":
            response = answer_query(user_input)
            print("Agent:", response)

        # -------- HIGH INTENT FLOW --------
        elif intent == "high_intent" or state["stage"] == "collecting":

            state["stage"] = "collecting"

            if not state["name"]:
                state["name"] = input("Agent: Please enter your name: ")
                continue

            if not state["email"]:
                state["email"] = input("Agent: Please enter your email: ")
                continue

            if not state["platform"]:
                state["platform"] = input("Agent: Which platform do you create on? (YouTube/Instagram): ")
                continue

            # ✅ Call tool only after collecting all data
            mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )

            print("Agent: 🎉 You're all set! Our team will contact you soon.")

            # Reset state
            state["name"] = None
            state["email"] = None
            state["platform"] = None
            state["stage"] = "start"

        # -------- UNKNOWN --------
        else:
            print("Agent: Sorry, I didn't understand. Can you rephrase?")

# ---------------- RUN ----------------
if __name__ == "__main__":
    run_agent()