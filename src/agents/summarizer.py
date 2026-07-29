import json
from src.agents.client import get_gemini_client, get_default_model

def summarize_table_schema(table_name: str, table_info: dict) -> str:
    """Generates a one-sentence business summary of a table's schema."""
    client = get_gemini_client()
    model = get_default_model()
    
    # Format the schema details for the prompt
    columns_info = []
    for col in table_info.get("columns", []):
        columns_info.append(f"- {col['column_name']} ({col['data_type']})")
    
    fks_info = []
    for fk in table_info.get("foreign_keys", []):
        fks_info.append(f"- {fk['foreign_column']} references {fk['primary_table']}({fk['primary_column']})")
        
    prompt = f"""
You are a Database Architect. 
Provide a concise, one-sentence business summary explaining what entity, process, or relationship this table represents in a relational database.

Table Name: {table_name}
Columns:
{chr(10).join(columns_info)}

Foreign Keys:
{chr(10).join(fks_info)}

One-sentence business summary:
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": 0.0}
    )
    
    return response.text.strip().replace('"', '')

def summarize_results(user_query: str, sql: str, results: list) -> str:
    """Summarizes SQL execution results into a human-friendly natural language response."""
    client = get_gemini_client()
    model = get_default_model()
    
    # Limit output length to prevent overloading context in extreme cases
    serialized_results = json.dumps(results[:100], default=str, indent=2)
    
    prompt = f"""
You are a helpful and intelligent data assistant.
Your job is to answer the user's natural language query using the provided SQL and the exact results retrieved from a PostgreSQL database.

User Query: "{user_query}"
SQL Executed: `{sql}`
Raw Database Results:
{serialized_results}

Create a clean, human-readable, and natural language response that directly answers the user's query. 
Use markdown tables or formatting where appropriate to make the data easy to read. 
If the results are empty, politely state that no matching records were found.
"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": 0.2}
    )
    
    return response.text.strip()
