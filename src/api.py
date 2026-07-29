import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.pipeline.live import execute_query
from src.pipeline.offline import run_offline_preprocessing

app = FastAPI(title="Query-ChatBot API")

# Request schemas
class QueryRequest(BaseModel):
    query: str

# Endpoints
@app.post("/api/query")
def post_query(request: QueryRequest):
    try:
        result = execute_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/preprocess")
def post_preprocess():
    try:
        run_offline_preprocessing()
        return {"status": "success", "message": "Database schema preprocessing completed."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serves the static single-page app
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.get("/")
def get_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)
