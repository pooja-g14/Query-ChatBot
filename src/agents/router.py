import json
from pydantic import BaseModel, Field
from typing import List
from src.agents.client import get_gemini_client, get_default_model

class RoutedTables(BaseModel):
    tables: List[str] = Field(description="List of primary tables required to answer the query. If no tables are relevant, return an empty list.")

def route_query(user_query: str, router_map: dict) -> List[str]:
    """Uses Gemini to identify the primary tables required for a user's query based on the router map."""
    client = get_gemini_client()
    model = get_default_model()
    
    # Format the router map for the prompt
    formatted_map = json.dumps(router_map, indent=2)
    
    prompt = f"""
You are a Pre-Router for a Text-to-SQL system.
Your job is to analyze the user's natural language query and decide which tables from the database are primary requirements to answer the query.

Here is the database schema description map (table_name to description):
{formatted_map}

User Query: "{user_query}"

Analyze the user's query and output a JSON list of table names that are needed to write the SQL query. Choose only the tables that are explicitly or implicitly referenced. Do not include extra tables.
"""
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": RoutedTables,
            "temperature": 0.0
        }
    )
    
    try:
        # Parse the JSON response
        result = json.loads(response.text)
        # Filter to only return tables that actually exist in the router map (to avoid hallucinated tables)
        valid_tables = [table for table in result.get("tables", []) if table in router_map]
        return valid_tables
    except Exception as e:
        # Fallback to returning empty list on failure
        return []
