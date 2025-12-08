from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/providers")
def get_providers():
    query = """
    MATCH (v:ServiceProvider)
    RETURN v.label AS serviceProvider ORDER BY serviceProvider
    """
    result = run_query(query)
    return [r["serviceProvider"] for r in result]
