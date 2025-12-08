from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/categories")
def get_categories():
    query = """
    MATCH (c:CloudCategory)
    RETURN c.label AS category ORDER BY category
    """
    result = run_query(query)
    return [r["category"] for r in result]
