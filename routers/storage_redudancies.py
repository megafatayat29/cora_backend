from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/storage/redundancies")
def get_storage_redundancies():
    query = """
    MATCH (s:StorageOffering)
    RETURN DISTINCT s.redundancy AS redundancy
    ORDER BY redundancy
    """
    result = run_query(query)
    return [r["redundancy"] for r in result]
