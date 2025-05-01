
from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, SAFE_PROMPT_PREFIX

client = Groq(api_key=GROQ_API_KEY)

ROLE_PROMPTS = {
    "child": "Use simple words. Always be very positive, fun, simple, and safe. Use simple words and lots of encouragement.",
    "teen": "Speak like a helpful older sibling. Use examples.Be motivating, creative, slightly casual, and always positive. Help them think smartly.",
    "mature": "Respond like a knowledgeable mentor with clarity and depth. Be inspiring, career-focused, and offer mature advice while being positive.",
}

def ask_chatbot(user_input: str, role: str = "child") -> str:
    role_prompt = ROLE_PROMPTS.get(role.lower(), "")
    full_system_prompt = f"{SAFE_PROMPT_PREFIX}\n{role_prompt}"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()