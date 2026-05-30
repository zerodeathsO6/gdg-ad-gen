from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import dotenv

config = dotenv.dotenv_values(".env")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your Firebase URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=config["API_KEY"])


# Define what the incoming data looks like
class CampaignRequest(BaseModel):
    brand_name: str
    tone: str


SYSTEM_INST = (
    "You are a brilliant, highly sarcastic, and witty marketing executive living in Guwahati, Assam. "
    "Your job is to create a hyper-local social media advertisement for the business name provided by the user.\n\n"
    "CRITICAL RULES:\n"
    "1. You must heavily use local context, inside jokes, and landmarks (e.g., traffic at Ganeshguri or Paltan Bazar, "
    "hanging out at Dighalipukhuri or GS Road, typical local college stereotypes, vs. Fancy Bazar bargain hunters).\n"
    "2. The advertisement must match the specific tone requested by the user.\n"
    "3. Keep the output punchy, under 120 words, structured for a social media post, and use emojis naturally.\n"
    "4. Blend English with standard local phrasing or slang seamlessly if it elevates the humor."
)


@app.post("/generate")
async def generate_campaign(request: CampaignRequest):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-3.1-flash-lite",
            system_instruction=SYSTEM_INST,
        )

        prompt = (
            f"Create a campaign for '{request.brand_name}' with a {request.tone} vibe."
        )
        response = model.generate_content(prompt)

        return {"success": True, "data": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
