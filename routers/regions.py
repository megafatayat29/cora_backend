from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/regions")
def get_regions():
    query = """
    MATCH (r:Region)
    RETURN r.label AS region ORDER BY region
    """
    result = run_query(query)
    return [r["region"] for r in result]
