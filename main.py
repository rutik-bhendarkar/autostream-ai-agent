import json

# ---------------- LOAD KNOWLEDGE BASE ----------------
def load_data():
    with open("knowledge_base.json") as f:
        return json.load(f)

data = load_data()

# ---------------- INTENT DETECTION ----------------
def detect_intent(user_input):
    text = user_input.lower()

    if "buy" in text or "subscribe" in text or "want" in text:
        return "high_intent"
    elif "price" in text or "plan" in text:
        return "inquiry"
    elif "hi" in text or "hello" in text:
        return "greeting"
    else:
        return "unknown"

# ---------------- RAG RESPONSE ----------------
def answer_query(query):
    query = query.lower()

    if "pro" in query:
        plan = data["plans"]["pro"]
        return f"Pro Plan costs {plan['price']}, offers {plan['videos']}, {plan['resolution']} and {plan.get('features', '')}."

    elif "basic" in query:
        plan = data["plans"]["basic"]
        return f"Basic Plan costs {plan['price']}, offers {plan['videos']} and {plan['resolution']}."

    elif "refund" in query:
        return data["policies"]["refund"]

    elif "support" in query:
        return data["policies"]["support"]

    else:
        return "We offer Basic and Pro plans. Ask me about pricing or features."

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
    print("🤖 AutoStream AI Agent Started (type 'exit' to stop)\n")

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

            # ✅ All details collected → call tool
            mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )

            print("Agent: 🎉 You're all set! Our team will contact you soon.")

            # Reset for next user
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