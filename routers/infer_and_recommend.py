from fastapi import APIRouter
from pydantic import BaseModel
from nlp_inference import extract_entities
import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

router = APIRouter()

class TextRequest(BaseModel):
    text: str


@router.post("/infer_and_recommend")
def infer_and_recommend(req: TextRequest):

    # --- STEP 1: Extract entities using your ML model ---
    entities = extract_entities(req.text)

    # --- STEP 2: Build payload for /recommend ---
    payload = {
        "industry": entities["industry"] or "",
        "serviceProvider": entities["serviceProvider"],
        "region": entities["region"],
        "purpose": entities["purpose"],
        "scale": entities["scale"] or "",
        "ranking_preference": "termurah",
        "price_limit": 0,
        "limit": 10
    }

    # --- STEP 3: Call existing /recommend endpoint ---
    RECOMMEND_ENDPOINT = f"{BASE_URL}/recommend"
    response = requests.post(RECOMMEND_ENDPOINT, json=payload)

    # --- STEP 4: Return combined result ---
    return {
        "entities": entities,
        "payload": payload,
        "recommendation": response.json()
    }
