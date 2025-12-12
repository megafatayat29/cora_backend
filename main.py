from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import storage_class, infer_and_recommend
from routers import industries, regions, categories, purposes, scales, recommend, stats, provider, instance_search as instance, recommend_storage, storage_access_pattern, storage_redudancies, chatbot

app = FastAPI(title="CORA – Cloud Recommender API")

# === CORS untuk frontend Vite di localhost:5173 ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(industries.router)
app.include_router(provider.router)
app.include_router(regions.router)
app.include_router(categories.router)
app.include_router(purposes.router)
app.include_router(scales.router)
app.include_router(recommend.router)
app.include_router(stats.router)
app.include_router(instance.router)
app.include_router(recommend_storage.router)
app.include_router(storage_redudancies.router)
app.include_router(storage_access_pattern.router)
app.include_router(storage_class.router)
app.include_router(chatbot.router)
app.include_router(infer_and_recommend.router)
