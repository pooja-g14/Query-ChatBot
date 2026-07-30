# Query-ChatBot

Features:
- Fetches the schema based on LLM response
- Uses LLM to generate SQL queries from the fetched schema and the user's question
- Uses PostgreSQL to execute queries
- Uses LLM to craft human-readable responses

## Run Preprocessing (Pipeline 1)

Before launching the chatbot or the web server, you must run the offline preprocessor to inspect your database structure, calculate fingerprints, and cache business summaries:

```bash
python main.py preprocess
```

*Note: You should rerun this command whenever your database schema changes (e.g., after running new migrations).*

## Running the Application

You can interact with the system either via the browser or the CLI.

### Option A: Launch the Web UI (FastAPI Server)

To start the local web application:
```bash
python main.py serve
```
By default, the server will start on **`http://127.0.0.1:8000/`**. Open this URL in your web browser to access the premium query interface.

### Option B: Query via CLI

To run a query directly in your terminal:
```bash
python main.py query "Your natural language question here"
```

## Project Structure

```
.
├── main.py                   # CLI entry point (preprocess, query, and serve commands)
├── requirements.txt          # Python dependencies
├── setup.md                  # Setup instructions and configuration details
├── README.md                 # Project overview and usage guidelines
├── data/                     # Extracted database schema metadata and caching
│   ├── fk_graph.json         # Database foreign key relationship graph
│   ├── router_map.json       # Topic-to-table routing index for the LLM router
│   └── schema_manifest.json  # Database table schemas and descriptions
├── test/                     # Testing and sample data
│   └── sample_data.md        # SQL DDL scripts and mock datasets
└── src/                      # Source code for the application
    ├── api.py                # FastAPI server endpoints and static frontend hosting
    ├── agents/               # LLM-powered specialized agents
    │   ├── client.py         # Gemini API client wrapper
    │   ├── router.py         # Agent that maps natural language queries to relevant tables
    │   ├── sql_writer.py     # Agent that writes PostgreSQL queries based on schemas
    │   └── summarizer.py     # Agent that formats database results into plain English
    ├── database/             # Database interface modules
    │   ├── connection.py     # PostgreSQL connection utility
    │   └── extractor.py      # Extraction functions for schema definition and metadata
    ├── pipeline/             # Pipeline orchestration
    │   ├── live.py           # Orchestrates real-time query parsing, routing, and execution
    │   └── offline.py        # Builds offline schema definitions and caches metadata
    ├── static/               # Web application frontend
    │   └── index.html        # Chatbot single-page user interface
    └── utils/                # Common utilities
        ├── graph.py          # Helper for dependency analysis and topological sorting
        └── manifest.py       # Helper for loading and writing schema manifests
```
