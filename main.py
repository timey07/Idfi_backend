from fastapi import FastAPI, Request
import httpx
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

@app.post("/analyze")
async def analyze(request: Request):
    try:
        image_data = await request.body()

        url = f"{AZURE_ENDPOINT}/vision/v3.2/analyze?visualFeatures=Objects,Tags,Description,Categories"

        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": AZURE_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, content=image_data)

        return response.json()
    except Exception as e:
        return {"error": str(e)}

