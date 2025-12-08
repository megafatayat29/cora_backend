from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/scales")
def get_scales():
    query = """
    MATCH (s:Scale)
    RETURN s.label AS scale ORDER BY scale
    """
    result = run_query(query)
    return [r["scale"] for r in result]
