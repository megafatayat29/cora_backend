from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import os
import requests

from config import get_settings

router = APIRouter(tags=["chatbot"])

# ==== KONFIGURASI HUGGINGFACE DARI ENV ====
settings = get_settings()
HF_TOKEN = settings.HF_TOKEN
HF_MODEL = "meta-llama/Llama-3.3-70B-Instruct"


class Message(BaseModel):
    role: str      # "user" atau "assistant"
    content: str


class ChatRequest(BaseModel):
    history: List[Message]


@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    """
    Endpoint untuk chatbot CORA.
    FE mengirim history, backend memanggil HF Router, lalu mengembalikan 1 balasan.
    """
    if not HF_TOKEN:
        return {"reply": "HF_TOKEN belum diset di server."}

    # === system prompt seperti di backend_chat.py ===
    system_prompt = (
        "You are CORA, a friendly customer-service-style assistant specializing in cloud computing. "
        "Jawab SELALU dalam Bahasa Indonesia yang ramah, jelas, dan terstruktur. "
        "FOKUS UTAMA kamu adalah tiga cloud provider saja: "
        "Amazon Web Services (AWS), Google Cloud Platform (GCP), dan Alibaba Cloud. "
        "Saat menjelaskan layanan, harga, region, atau best practice, "
        "selalu gunakan contoh dari ketiga provider ini saja. "
        "Jika pengguna bertanya tentang provider lain (misalnya Azure, Oracle Cloud, DigitalOcean, dsb.), "
        "jawab dengan sopan bahwa CORA saat ini hanya mendukung AWS, GCP, dan Alibaba Cloud, "
        "lalu bantu berikan alternatif yang setara dari salah satu dari tiga provider tersebut. "
        "JANGAN menyebut atau menjelaskan detail provider lain di luar tiga itu."
    )

    # riwayat chat dari FE → format messages untuk HF
    messages = [{"role": "system", "content": system_prompt}]
    for m in req.history:
        msg_role = "user" if m.role == "user" else "assistant"
        messages.append({"role": msg_role, "content": m.content})

    payload = {
        "model": HF_MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()

        choices = data.get("choices")
        if choices and "message" in choices[0]:
            reply = choices[0]["message"].get("content", "")
            reply = reply.strip() or "(Model tidak mengembalikan teks.)"
            return {"reply": reply}

        # kalau struktur respons aneh
        return {"reply": f"Respons tidak terduga dari Hugging Face: {data}"}

    except requests.HTTPError as http_err:
        status = http_err.response.status_code if http_err.response is not None else "unknown"
        body = ""
        try:
            body = http_err.response.json()
        except Exception:
            if http_err.response is not None:
                body = http_err.response.text
        return {"reply": f"Error HTTP {status} dari Hugging Face: {body}"}

    except Exception as e:
        return {"reply": f"Terjadi error memanggil Hugging Face API: {e}"}