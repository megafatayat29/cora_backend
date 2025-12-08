from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from neo4j_connector import run_query

router = APIRouter()

class StorageRecommendRequest(BaseModel):
    serviceProvider: Optional[List[str]] = None
    region: Optional[List[str]] = None
    storageClass: Optional[List[str]] = None
    redundancy: Optional[List[str]] = None
    price_limit: float = 0.0
    limit: int = 10

@router.post("/recommend/storage")
def recommend_storage(req: StorageRecommendRequest):

    filters = ""

    if req.serviceProvider:
        filters += " AND p.label IN $serviceProvider"
    if req.region:
        filters += " AND r.label IN $region"
    if req.storageClass:
        filters += " AND s.storageClass IN $storageClass"
    if req.redundancy:
        filters += " AND s.redundancy IN $redundancy"
    if req.price_limit > 0:
        filters += " AND s.priceUsdUnit <= $price_limit"

    query = f"""
    MATCH (s:StorageOffering)-[:storageOfferedBy]->(p:ServiceProvider)
    MATCH (s)-[:storageAvailableInRegion]->(r:Region)
    WHERE 1=1
    {filters}
    RETURN 
        s.rdfs__label AS name,
        p.label AS provider,
        r.label AS region,
        s.storageClass AS storageClass,
        s.storageType AS storageType,
        s.redundancy AS redundancy,
        s.accessPattern AS accessPattern,
        s.priceUsdUnit AS price
    ORDER BY s.priceUsdUnit ASC
    LIMIT $limit
    """

    return run_query(query, req.dict())
