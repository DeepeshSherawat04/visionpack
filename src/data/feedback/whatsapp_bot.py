# visionpack-ai/src/data/feedback/whatsapp_bot.py
from fastapi import APIRouter, Request
from twilio.twiml.messaging_response import MessagingResponse
import json, os

router = APIRouter()

@router.post("/feedback")
async def feedback(request: Request):
    form = await request.form()
    sender = form.get("From", "")
    msg = form.get("Body", "").lower()

    resp = MessagingResponse()
    if msg in ["yes", "y"]:
        resp.message("✅ Thank you for confirming!")
    elif msg.startswith("no") or "correct" in msg:
        resp.message("❌ Please reply with correct class label (e.g. 'box')")
    else:
        resp.message("👋 Reply 'yes' if correct, 'no' if not.")

    os.makedirs("data/feedback", exist_ok=True)
    with open("data/feedback/log.json", "a") as f:
        f.write(json.dumps({"sender": sender, "msg": msg}) + "\n")

    return str(resp)
