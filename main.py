import sys
import argparse
from src.pipeline.offline import run_offline_preprocessing
from src.pipeline.live import execute_query
from logger import logger

def main():
    parser = argparse.ArgumentParser(description="Query-ChatBot: Dynamic Schema Text-to-SQL System")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands")
    
    # Preprocess command
    subparsers.add_parser("preprocess", help="Run the offline schema preprocessing pipeline")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Run the live query execution pipeline")
    query_parser.add_argument("text", type=str, help="The natural language query")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the FastAPI web server")
    serve_parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address to bind to")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    if args.command == "preprocess":
        try:
            run_offline_preprocessing()
        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            sys.exit(1)
            
    elif args.command == "query":
        try:
            result = execute_query(args.text)
            print("\n--- FINAL RESPONSE ---")
            print(result["response"])
            print("----------------------")
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            sys.exit(1)
 
    elif args.command == "serve":
        import uvicorn
        try:
            logger.info(f"Starting server on http://{args.host}:{args.port}")
            uvicorn.run("src.api:app", host=args.host, port=args.port, reload=True)
        except Exception as e:
            logger.error(f"Error starting server: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
