
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import ask_chatbot
from filters import input_is_safe, output_is_safe
from reinforcement import detect_positive_themes

app = FastAPI(
    title="Child Safe AI Mentor",
    description="A smart, safe, and positive AI mentor for kids and teens.",
    version="1.0"
)

class UserQuery(BaseModel):
    user_input: str
    role: str  # child, teen, or mature

@app.post("/ask")
def ask_mentor(query: UserQuery):
    if not input_is_safe(query.user_input):
        raise HTTPException(status_code=400, detail="That question may not be safe to ask.")

    response = ask_chatbot(query.user_input, query.role)

    if not output_is_safe(response):
        raise HTTPException(status_code=400, detail="Sorry, the response could not be shown.")

    badge = detect_positive_themes(response)

    return {"reply": response, "badge": badge}