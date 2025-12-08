from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/stats")
def get_stats():
    q = """
    MATCH (s:Service)
    WITH count(s) AS services

    MATCH (p:ServiceProvider)
    WITH services, count(p) AS providers

    MATCH (r:Region)
    WITH services, providers, count(r) AS regions

    MATCH (i:Industry)
    WITH services, providers, regions, count(i) AS industries

    MATCH (c:Cluster)
    WITH services, providers, regions, industries, count(c) AS clusters

    MATCH (cat:CloudCategory)
    RETURN 
      services,
      providers,
      regions,
      industries,
      clusters,
      count(cat) AS categories
    """
    return run_query(q)[0]
