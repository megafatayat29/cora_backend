from neo4j import GraphDatabase
from config import get_settings

settings = get_settings()

driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
)

def run_query(query: str, params: dict = {}):
    with driver.session() as session:
        result = session.run(query, params)
        return [r.data() for r in result]
