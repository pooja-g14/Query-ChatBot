from src.database.extractor import extract_full_schema
from src.agents.summarizer import summarize_table_schema
from src.utils.manifest import load_manifest, save_manifest, save_router_map, save_fk_graph

def run_offline_preprocessing():
    """Runs the offline schema preprocessing pipeline."""
    print("Starting schema preprocessing...")
    
    # 1. Extract current database schema metadata
    current_schema = extract_full_schema()
    print(f"Extracted schema details for {len(current_schema)} table(s).")
    
    # 2. Load previous manifest
    old_manifest = load_manifest()
    
    new_manifest = {}
    router_map = {}
    fk_graph = {}
    
    summarized_count = 0
    reused_count = 0
    
    # 3. Compare tables and generate/reuse summaries
    for table_name, details in current_schema.items():
        # Get matching hash from old manifest
        old_table_details = old_manifest.get(table_name)
        
        summary = None
        if old_table_details and old_table_details.get("md5") == details["md5"]:
            # Match! Reuse old summary
            summary = old_table_details.get("summary")
            reused_count += 1
        
        # If no summary exists (or structural hash mismatch), generate it
        if not summary:
            print(f"Table '{table_name}' has changed or is new. Summarizing using LLM...")
            summary = summarize_table_schema(table_name, details)
            summarized_count += 1
            
        # Update manifest entry
        new_manifest[table_name] = {
            "md5": details["md5"],
            "ddl": details["ddl"],
            "referenced_tables": details["referenced_tables"],
            "summary": summary
        }
        
        # Update Artifact A map
        router_map[table_name] = summary
        
        # Update Artifact B map
        fk_graph[table_name] = details["referenced_tables"]
        
    # 4. Save artifacts
    save_manifest(new_manifest)
    save_router_map(router_map)
    save_fk_graph(fk_graph)
    
    print("Preprocessing completed successfully!")
    print(f"Summary: {reused_count} tables reused, {summarized_count} tables newly summarized.")
    print("Artifacts generated:")
    print("- Artifact A (router_map.json)")
    print("- Artifact B (fk_graph.json)")
    print("- Cached manifest (schema_manifest.json)")
