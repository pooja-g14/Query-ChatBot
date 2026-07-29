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

---

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
Example:
```bash
python main.py query "Show me all users who signed up last month"
```