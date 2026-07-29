def expand_tables(primary_tables: list, fk_graph: dict) -> list:
    """Recursively expands a list of primary tables to include all referenced tables from foreign keys."""
    expanded = list(primary_tables)
    queue = list(primary_tables)
    visited = set(primary_tables)
    
    while queue:
        current_table = queue.pop(0)
        # Look up referenced tables from this table
        referenced = fk_graph.get(current_table, [])
        for ref in referenced:
            if ref not in visited:
                visited.add(ref)
                expanded.append(ref)
                queue.append(ref)
                
    return expanded
