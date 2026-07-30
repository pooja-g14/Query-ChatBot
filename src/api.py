import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.pipeline.live import execute_query
from src.pipeline.offline import run_offline_preprocessing
from logger import logger

app = FastAPI(title="Query-ChatBot API")

# Request schemas
class QueryRequest(BaseModel):
    query: str

# Endpoints
@app.post("/api/query")
def post_query(request: QueryRequest):
    logger.info(f"API Request: /api/query with query: '{request.query}'")
    try:
        result = execute_query(request.query)
        logger.info("API Request: /api/query processed successfully.")
        return result
    except Exception as e:
        logger.error(f"API Error processing /api/query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/preprocess")
def post_preprocess():
    logger.info("API Request: /api/preprocess initiated.")
    try:
        run_offline_preprocessing()
        logger.info("API Request: /api/preprocess completed successfully.")
        return {"status": "success", "message": "Database schema preprocessing completed."}
    except Exception as e:
        logger.error(f"API Error processing /api/preprocess: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serves the static single-page app
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.get("/")
def get_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        logger.error(f"Frontend file not found at: {index_path}")
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)
