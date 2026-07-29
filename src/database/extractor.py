import hashlib
import json
from src.database.connection import get_db_cursor

def get_all_tables():
    """Fetches all table names in the public schema."""
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """
    with get_db_cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        return [row['table_name'] for row in rows]

def get_table_schema_details(table_name):
    """Fetches details of all columns for a given table."""
    query = """
        SELECT 
            c.column_name, 
            c.data_type, 
            c.is_nullable,
            c.column_default,
            (
                SELECT count(*) 
                FROM information_schema.table_constraints tc 
                JOIN information_schema.key_column_usage kcu 
                  ON tc.constraint_name = kcu.constraint_name 
                 AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY' 
                  AND tc.table_name = c.table_name 
                  AND kcu.column_name = c.column_name
            ) > 0 AS is_primary
        FROM information_schema.columns c
        WHERE c.table_schema = 'public' AND c.table_name = %s
        ORDER BY c.ordinal_position;
    """
    with get_db_cursor() as cur:
        cur.execute(query, (table_name,))
        return cur.fetchall()

def get_foreign_keys():
    """Fetches all foreign key relationships in the public schema."""
    query = """
        SELECT
            kcu.table_name AS foreign_table,
            kcu.column_name AS foreign_column,
            ccu.table_name AS primary_table,
            ccu.column_name AS primary_column
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public';
    """
    with get_db_cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def compute_table_hash(columns, foreign_keys):
    """Computes a stable MD5 hash representing the table schema structure."""
    # Sort columns by name to ensure stable hash
    sorted_cols = sorted(columns, key=lambda c: c['column_name'])
    # Filter and sort foreign keys related to this table
    sorted_fks = sorted(foreign_keys, key=lambda f: (f['foreign_column'], f['primary_table'], f['primary_column']))
    
    structure = {
        "columns": [
            {
                "column_name": c["column_name"],
                "data_type": c["data_type"],
                "is_nullable": c["is_nullable"],
                "is_primary": c["is_primary"]
            } for c in sorted_cols
        ],
        "foreign_keys": [
            {
                "fk_col": fk["foreign_column"],
                "pk_table": fk["primary_table"],
                "pk_col": fk["primary_column"]
            } for fk in sorted_fks
        ]
    }
    
    serialized = json.dumps(structure, sort_keys=True)
    return hashlib.md5(serialized.encode('utf-8')).hexdigest()

def generate_ddl(table_name, columns, foreign_keys):
    """Generates a clean DDL string for LLM prompt context."""
    ddl_parts = []
    pk_cols = []
    
    for col in columns:
        col_def = f"  {col['column_name']} {col['data_type']}"
        if col['is_nullable'] == 'NO':
            col_def += " NOT NULL"
        if col['is_primary']:
            pk_cols.append(col['column_name'])
        ddl_parts.append(col_def)
        
    if pk_cols:
        ddl_parts.append(f"  PRIMARY KEY ({', '.join(pk_cols)})")
        
    for fk in foreign_keys:
        ddl_parts.append(
            f"  FOREIGN KEY ({fk['foreign_column']}) REFERENCES {fk['primary_table']}({fk['primary_column']})"
        )
        
    ddl = f"CREATE TABLE {table_name} (\n" + ",\n".join(ddl_parts) + "\n);"
    return ddl

def extract_full_schema():
    """Extracts all table details, computes hashes, and generates DDLs."""
    tables = get_all_tables()
    fks = get_foreign_keys()
    
    schema_data = {}
    for table in tables:
        cols = get_table_schema_details(table)
        table_fks = [fk for fk in fks if fk['foreign_table'] == table]
        
        md5_hash = compute_table_hash(cols, table_fks)
        ddl = generate_ddl(table, cols, table_fks)
        
        # Referenced tables from this table (for foreign key graph)
        referenced = list(set([fk['primary_table'] for fk in table_fks]))
        
        schema_data[table] = {
            "columns": [dict(c) for c in cols],
            "foreign_keys": [dict(f) for f in table_fks],
            "md5": md5_hash,
            "ddl": ddl,
            "referenced_tables": referenced
        }
    return schema_data
