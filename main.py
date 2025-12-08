from fastapi import FastAPI
from routers import storage_class
from routers import industries, regions, categories, purposes, scales, recommend, stats, provider, instance_search as instance, recommend_storage, storage_access_pattern, storage_redudancies

app = FastAPI(title="CORA – Cloud Recommender API")

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
