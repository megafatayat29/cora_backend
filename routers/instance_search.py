from fastapi import APIRouter
from pydantic import BaseModel
from neo4j_connector import run_query

router = APIRouter()

class InstanceSearch(BaseModel):
    query: str

@router.post("/instance/search")
def search_instance(req: InstanceSearch):
    query = """
    MATCH (s:Service)-[:hasSpec]->(spec:Specification)
    MATCH (s)-[:offeredBy]->(p:ServiceProvider)
    MATCH (s)-[:availableInRegion]->(r:Region)
    MATCH (s)-[:hasCloudCategory]->(c:CloudCategory)
    MATCH (s)-[:category]->(cl:Cluster)
    MATCH (s)-[:hasScale]->(sc:Scale)
    MATCH (i:Industry)-[:hasRequirementProfile]->(reqProf)
    WHERE 
        toLower(s.instanceType) CONTAINS toLower($query)
        AND spec.vCPU >= reqProf.minCPU 
        AND spec.ramGiB >= reqProf.minRAMGiB
    RETURN 
        s.instanceType AS instance,
        p.label AS provider,
        spec.vCPU AS vcpu,
        spec.ramGiB AS ram,
        spec.priceUsdHour AS price,
        c.label AS category,
        collect(DISTINCT sc.label) AS scales,
        collect(DISTINCT cl.label) AS purposes,
        collect(DISTINCT r.label) AS regions,
        collect(DISTINCT i.name) AS industries
    """
    return run_query(query, {"query": req.query})
