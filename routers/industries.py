from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/industries")
def get_industries():
    query = """
    MATCH (i:Industry)
    RETURN i.name AS industry ORDER BY industry
    """
    result = run_query(query)
    return [r["industry"] for r in result]
