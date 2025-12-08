from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/purposes")
def get_purposes():
    query = """
    MATCH (c:Cluster)
    RETURN c.label AS purpose ORDER BY purpose
    """
    result = run_query(query)
    return [r["purpose"] for r in result]
