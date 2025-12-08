from fastapi import APIRouter
from neo4j_connector import run_query

router = APIRouter()

@router.get("/storage/class")
def get_storage_types():
    query = """
    MATCH (s:StorageOffering)
    RETURN DISTINCT s.storageClass AS storageClass
    ORDER BY storageClass
    """
    result = run_query(query)
    return [r["storageClass"] for r in result]
