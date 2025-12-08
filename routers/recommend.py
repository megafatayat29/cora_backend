from fastapi import APIRouter
from pydantic import BaseModel
from neo4j_connector import run_query
from typing import List, Optional

router = APIRouter()

class RecommendRequest(BaseModel):
    industry: str
    serviceProvider: Optional[List[str]] = None
    region: Optional[List[str]] = None
    purpose: Optional[List[str]] = None
    scale: Optional[str] = None
    ranking_preference: str = "termurah"
    price_limit: float = 0.0
    limit: int = 10


@router.post("/recommend")
def get_recommendations(req: RecommendRequest):

    filters = ""

    if req.serviceProvider:
        filters += " AND v.label IN $serviceProvider"
    if req.region:
        filters += " AND r.label IN $region"
    if req.purpose:
        filters += " AND cl.label IN $purpose"
    if req.scale:
        filters += " AND sc.label = $scale"
    if req.price_limit > 0:
        filters += " AND spec.priceUsdHour <= $price_limit"

    # Ranking preference
    order_by = "spec.priceUsdHour ASC"
    if req.ranking_preference == "terkuat":
        order_by = "spec.vCPU DESC, spec.ramGiB DESC"
    elif req.ranking_preference == "balanced":
        order_by = "((spec.vCPU + spec.ramGiB) / spec.priceUsdHour) DESC"

    query = f"""
    MATCH (i:Industry {{name: $industry}})-[:hasRequirementProfile]->(req)
    MATCH (s:Service)-[:hasSpec]->(spec:Specification)
    MATCH (s)-[:offeredBy]->(v:ServiceProvider)
    MATCH (s)-[:availableInRegion]->(r:Region)
    MATCH (s)-[:hasCloudCategory]->(ccat:CloudCategory)
    WHERE ccat.label = "Compute"
    MATCH (s)-[:category]->(cl:Cluster)
    MATCH (s)-[:hasScale]->(sc:Scale)
    WHERE spec.vCPU >= req.minCPU
    AND spec.ramGiB >= req.minRAMGiB
    {filters}
    RETURN 
        s.instanceType AS instance,
        v.label AS serviceProvider,
        r.label AS region,
        spec.vCPU AS vcpu,
        spec.ramGiB AS ram,
        spec.priceUsdHour AS price,
        cl.label AS purpose,
        sc.label AS scale
    ORDER BY {order_by}
    LIMIT $limit
    """

    params = req.dict()
    return run_query(query, params)
