import json
import psycopg2
from pydantic import BaseModel, Field
from google.genai import types
from src.agents.client import get_gemini_client, get_default_model
from src.database.connection import get_db_cursor

class GeneratedSQL(BaseModel):
    sql: str = Field(description="The complete, valid, executable PostgreSQL SQL query. Do not wrap in markdown quotes in the JSON string.")

def validate_sql(sql: str) -> str:
    """Validates the SQL query using PostgreSQL EXPLAIN. 
    Returns None if valid, or the error message if invalid."""
    try:
        with get_db_cursor() as cur:
            # We use EXPLAIN to validate the syntax and schema correctness without executing the query
            cur.execute(f"EXPLAIN {sql}")
        return None
    except psycopg2.Error as e:
        return str(e)

def write_sql(user_query: str, ddls: str, max_retries: int = 3) -> str:
    """Generates and self-corrects PostgreSQL SQL queries using Gemini."""
    client = get_gemini_client()
    model = get_default_model()
    
    system_instruction = """
    You are an expert SQL Writer for PostgreSQL.
    Your goal is to convert natural language queries into valid PostgreSQL SQL.
    You must construct the query using ONLY the tables and columns defined in the provided DDL schema.
    Ensure your query uses correct PostgreSQL syntax (e.g., proper quotes, case sensitivity if tables/columns require it, join conditions, and PostgreSQL-specific functions).
    Return ONLY the SQL query.
    """

    history = []
    for attempt in range(1, max_retries + 1):
        # Build prompt
        prompt_parts = [
            f"Here are the DDL schemas for the relevant tables:\n{ddls}\n",
            f"User Query: {user_query}\n"
        ]
        
        if history:
            prompt_parts.append("Previous attempts failed validation. Please correct the SQL query based on the errors below:")
            for prev_sql, error in history:
                prompt_parts.append(f"Failed SQL:\n{prev_sql}\nError message:\n{error}\n")
                
        prompt = "\n".join(prompt_parts)
        
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_json_schema=GeneratedSQL.model_json_schema(),
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                temperature=0.0
            )
        )
        
        try:
            res_json = json.loads(response.text)
            sql = res_json.get("sql", "").strip()
            # Remove trailing semicolon if present (or keep it, both work)
        except Exception as e:
            # If JSON parsing failed, try using response.text directly (fallback)
            sql = response.text.strip()
            
        if not sql:
            continue
            
        # Validate SQL
        err = validate_sql(sql)
        if not err:
            # SQL is valid!
            return sql
            
        # SQL failed, log and retry
        history.append((sql, err))
        
    # If we exhausted retries, raise an exception or return the last generated SQL (the pipeline will fail/handle it)
    if history:
        raise ValueError(f"Failed to generate valid SQL after {max_retries} attempts. Last error: {history[-1][1]}")
    else:
        raise ValueError("Could not generate SQL query.")
