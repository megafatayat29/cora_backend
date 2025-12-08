from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/storage/access-patterns")
def get_storage_access_patterns():
    query = """
    MATCH (s:StorageOffering)
    RETURN DISTINCT s.accessPattern AS accessPattern
    ORDER BY accessPattern
    """
    result = run_query(query)
    return [r["accessPattern"] for r in result]
