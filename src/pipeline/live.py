import json
from src.agents.router import route_query
from src.utils.graph import expand_tables
from src.agents.sql_writer import write_sql
from src.agents.summarizer import summarize_results
from src.database.connection import get_db_cursor
from src.utils.manifest import load_router_map, load_fk_graph, load_manifest

def execute_query(user_query: str) -> dict:
    """Orchestrates Pipeline 2: Live Text-to-SQL query execution pipeline."""
    # 1. Load artifacts
    router_map = load_router_map()
    fk_graph = load_fk_graph()
    manifest = load_manifest()
    
    if not router_map or not manifest:
        raise ValueError("System cache / artifacts are empty. Please run preprocessing first.")
        
    print(f"\n--- Processing Query: '{user_query}' ---")
    
    # Step 1: Pre-Router Table Selection
    print("Step 1: Identifying relevant tables...")
    primary_tables = route_query(user_query, router_map)
    print(f"-> Primary routed tables: {primary_tables}")
    
    if not primary_tables:
        print("-> No tables routed. Attempting to answer directly or querying default table schemas.")
        
    # Step 2: Foreign Key Auto-Expansion
    print("Step 2: Expanding dependencies via Foreign Key graph...")
    expanded_tables = expand_tables(primary_tables, fk_graph)
    print(f"-> Expanded tables: {expanded_tables}")
    
    # Step 3: Schema DDL Assembly
    print("Step 3: Assembling DDL context...")
    ddl_list = []
    for table in expanded_tables:
        if table in manifest:
            ddl_list.append(manifest[table]["ddl"])
    ddls = "\n\n".join(ddl_list)
    
    # Step 4: SQL Writing and Validation (Self-Correction Loop)
    print("Step 4: Writing and validating SQL query...")
    try:
        sql = write_sql(user_query, ddls)
        print(f"-> Generated Valid SQL:\n{sql}\n")
    except Exception as e:
        print(f"-> SQL generation failed: {e}")
        return {
            "query": user_query,
            "error": f"Failed to generate valid SQL: {e}",
            "response": "I encountered an error generating a valid database query."
        }
        
    # Step 5: Execute SQL against PostgreSQL
    print("Step 5: Executing query on PostgreSQL...")
    try:
        with get_db_cursor() as cur:
            cur.execute(sql)
            results = cur.fetchall()
            # Convert list of RealDictRow to standard list of dicts
            results = [dict(row) for row in results]
        print(f"-> Executed successfully, retrieved {len(results)} rows.")
    except Exception as e:
        print(f"-> Execution failed: {e}")
        return {
            "query": user_query,
            "sql": sql,
            "error": f"Database execution error: {e}",
            "response": "I generated a query but it failed to execute on the database."
        }
        
    # Step 6: Formulate Final Answer
    print("Step 6: Formulating natural language response...")
    response = summarize_results(user_query, sql, results)
    
    return {
        "query": user_query,
        "routed_tables": primary_tables,
        "expanded_tables": expanded_tables,
        "sql": sql,
        "results": results,
        "response": response
    }
