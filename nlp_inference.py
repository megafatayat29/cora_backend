from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from config import get_settings

settings = get_settings()
HF_TOKEN = settings.HF_TOKEN_NER
HF_REPO_ID = "megafatayat29/ner_cora_epoch10"

tokenizer = AutoTokenizer.from_pretrained(
    HF_REPO_ID, 
    token=HF_TOKEN
)
model = AutoModelForTokenClassification.from_pretrained(
    HF_REPO_ID, 
    token=HF_TOKEN
)

def ner_infer(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    preds = outputs.logits.argmax(dim=-1)[0]

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    labels = [model.config.id2label[int(p)] for p in preds]

    merged_tokens = []
    merged_labels = []

    current_word = ""
    current_label = None

    for token, label in zip(tokens, labels):
        if token.startswith("##"):
            # merge subword token into the previous word
            current_word += token[2:]
        else:
            # push previous word first
            if current_word:
                merged_tokens.append(current_word)
                merged_labels.append(current_label)
            current_word = token
            current_label = label

    # push last word
    if current_word:
        merged_tokens.append(current_word)
        merged_labels.append(current_label)

    return list(zip(merged_tokens, merged_labels))

def extract_entities(text):
    pairs = ner_infer(text)

    # remove noise tokens
    NOISE = {"[CLS]", "[SEP]", ".", ",", ";", ":"}
    pairs = [(w.lower(), l) for w, l in pairs if w not in NOISE]

    entities = {
        "industry": None,
        "serviceProvider": [],
        "region": [],
        "purpose": [],
        "scale": None
    }

    PURPOSE_MAP = {
        "data": "General Purpose",
        "analytics": "General Purpose",
        "machine": "Compute Optimized",
        "learning": "Compute Optimized",
        "storage": "Storage Optimized",
        "web": "General Purpose",
        "hosting": "General Purpose",
        "ai": "Accelerator Specialized",
        "compute": "Compute Optimized"
    }

    INDUSTRY_MAP = {
        # AI_ML
        "ai": "AI_ML",
        "artificial intelligence": "AI_ML",
        "machine learning": "AI_ML",
        "ml": "AI_ML",
        "deep learning": "AI_ML",

        # Agriculture
        "agriculture": "Agriculture",
        "farming": "Agriculture",
        "agri": "Agriculture",
        "agritech": "Agriculture",

        # Automotive
        "automotive": "Automotive",
        "car": "Automotive",
        "vehicle": "Automotive",
        "mobility": "Automotive",

        # Banking
        "banking": "Banking",
        "bank": "Banking",
        "finance": "Banking",
        "financial services": "Banking",

        # BigData_Analytics
        "big data": "BigData_Analytics",
        "analytics": "BigData_Analytics",
        "data analytics": "BigData_Analytics",
        "data science": "BigData_Analytics",

        # Cybersecurity
        "cybersecurity": "Cybersecurity",
        "security": "Cybersecurity",
        "infosec": "Cybersecurity",
        "threat detection": "Cybersecurity",

        # Ecommerce
        "ecommerce": "Ecommerce",
        "online store": "Ecommerce",
        "marketplace": "Ecommerce",
        "e-commerce": "Ecommerce",

        # Education
        "education": "Education",
        "school": "Education",
        "university": "Education",
        "edtech": "Education",

        # Energy
        "energy": "Energy",
        "oil": "Energy",
        "gas": "Energy",
        "power": "Energy",

        # Fintech
        "fintech": "Fintech",
        "payment": "Fintech",
        "payments": "Fintech",
        "wallet": "Fintech",
        "insurtech": "Fintech",

        # Gaming
        "gaming": "Gaming",
        "game": "Gaming",
        "esports": "Gaming",

        # Government
        "government": "Government",
        "public sector": "Government",

        # Healthcare
        "healthcare": "Healthcare",
        "health": "Healthcare",
        "medtech": "Healthcare",
        "hospital": "Healthcare",
        "clinic": "Healthcare",

        # IoT Platforms
        "iot": "IoT_Platforms",
        "internet of things": "IoT_Platforms",
        "sensor": "IoT_Platforms",
        "embedded": "IoT_Platforms",

        # Logistics
        "logistics": "Logistics",
        "delivery": "Logistics",
        "shipping": "Logistics",
        "supply chain": "Logistics",

        # Manufacturing
        "manufacturing": "Manufacturing",
        "factory": "Manufacturing",
        "industrial": "Manufacturing",

        # Media & Entertainment
        "media": "Media_and_Entertainment",
        "entertainment": "Media_and_Entertainment",
        "broadcast": "Media_and_Entertainment",
        "content": "Media_and_Entertainment",

        # Pharmaceutical
        "pharma": "Pharmaceutical",
        "pharmaceutical": "Pharmaceutical",
        "biotech": "Pharmaceutical",

        # Retail
        "retail": "Retail",
        "store": "Retail",
        "shop": "Retail",

        # Telecommunications
        "telecom": "Telecommunications",
        "telco": "Telecommunications",
        "telecommunications": "Telecommunications",
        "5g": "Telecommunications",
    }

    for w, label in pairs:

        if label == "B-INDUSTRY":
            if w in INDUSTRY_MAP:
                entities["industry"] = INDUSTRY_MAP[w]

        elif label == "B-PROVIDER":
            entities["serviceProvider"].append(w.upper())

        elif label == "B-REGION":
            entities["region"].append(w.title())

        elif label == "B-SCALE":
            entities["scale"] = w

        elif label == "B-PURPOSE":
            # convert to dropdown purpose
            if w in PURPOSE_MAP:
                entities["purpose"].append(PURPOSE_MAP[w])

    return entities
