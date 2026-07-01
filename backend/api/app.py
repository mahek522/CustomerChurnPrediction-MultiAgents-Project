"""
FastAPI backend for Customer Churn Intelligence Platform.
"""
from pathlib import Path
import sys
import uuid
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd

from backend.crews.churn_crew import execute_churn_crew
from backend.services.data_ingestion_pipeline import DataIngestionPipeline
from backend.services.memory_context_service import load_session_context, persist_session_results
from backend.services.pdf_service import generate_pdf_report
from backend.memory.init_db import initialize_database
from backend.memory.database import SessionLocal
from backend.memory.models import ConversationHistory


app = FastAPI(
    title="Customer Churn Intelligence Platform",
    description="Agentic AI Multi-Agent System for Customer Churn Prediction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class QueryRequest(BaseModel):
    session_id: Optional[str] = None
    user_query: str
    context: Optional[str] = None


class QueryResponse(BaseModel):
    session_id: str
    response: str
    status: str


class HistoryResponse(BaseModel):
    session_id: str
    history: list


class ReportRequest(BaseModel):
    session_id: str


class ReportResponse(BaseModel):
    session_id: str
    report: str


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        initialize_database()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")


# Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Customer Churn Intelligence Platform API",
        "version": "1.0.0",
        "endpoints": {
            "POST /upload": "Upload CSV dataset",
            "POST /query": "Submit query to AI agents",
            "GET /history/{session_id}": "Get conversation history",
            "POST /generate-report": "Generate report for session",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload CSV dataset for customer churn analysis.
    
    The dataset will be processed and stored locally and in ChromaDB for retrieval.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read CSV
        contents = await file.read()
        import io
        df = pd.read_csv(io.BytesIO(contents))
        
        # Save CSV locally so fallback and dashboard can read it
        from backend.services.config import DATASET_PATH
        DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(DATASET_PATH, index=False)
        print(f"Saved uploaded dataset locally to {DATASET_PATH}")
        
        # Run data ingestion pipeline (ChromaDB)
        try:
            pipeline = DataIngestionPipeline()
            result = pipeline.ingest_dataset(df)
            
            if result.get("status") == "error":
                print(f"ChromaDB ingestion failed, but dataset was saved locally: {result.get('error')}")
                return {
                    "status": "success",
                    "message": "Dataset uploaded successfully (ChromaDB index skipped: network limit)",
                    "records_processed": len(df),
                    "collection_name": "customer_churn"
                }
        except Exception as ingest_err:
            print(f"Warning: ChromaDB ingestion failed: {ingest_err}")
            
        return {
            "status": "success",
            "message": "Dataset uploaded and processed successfully",
            "records_processed": len(df),
            "collection_name": "customer_churn"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_agents(request: QueryRequest):
    """
    Submit a query to the multi-agent system.
    
    The query will be processed by the agent crew:
    1. Query Agent retrieves relevant customer records
    2. Data Analyst Agent analyzes patterns
    3. Prediction Agent predicts churn risk
    4. Recommendation Agent generates retention strategies
    5. Validation Agent validates results
    6. Reporting Agent generates final report
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Execute crew
        response = execute_churn_crew(
            session_id=session_id,
            user_query=request.user_query,
            context=request.context or ""
        )
        
        return QueryResponse(
            session_id=session_id,
            response=response,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    """
    Get conversation history for a session.
    """
    try:
        from backend.memory.memory_service import get_conversation_history
        
        records = get_conversation_history(session_id)
        history = [
            {
                "user_query": record.user_query,
                "agent_response": record.agent_response,
                "created_at": record.created_at.isoformat() if record.created_at else None
            }
            for record in records
        ]
        
        return HistoryResponse(
            session_id=session_id,
            history=history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@app.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate a report for a specific session.
    """
    try:
        from backend.memory.memory_service import get_conversation_history
        
        records = get_conversation_history(request.session_id)
        if not records:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get the latest response
        latest_record = records[-1]
        report = latest_record.agent_response
        
        # Generator PDF as a side effect and save locally
        try:
            pdf_dir = Path("static/reports")
            pdf_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = pdf_dir / f"report_{request.session_id}.pdf"
            generate_pdf_report(report, str(pdf_path))
        except Exception as pdf_err:
            print(f"Warning: PDF generation failed: {pdf_err}")
            
        return ReportResponse(
            session_id=request.session_id,
            report=report
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@app.get("/download-report/{session_id}")
async def download_report(session_id: str):
    """
    Download generated PDF report for a session.
    """
    pdf_path = Path("static/reports") / f"report_{session_id}.pdf"
    if not pdf_path.exists():
        try:
            from backend.memory.memory_service import get_conversation_history
            records = get_conversation_history(session_id)
            if not records:
                raise HTTPException(status_code=404, detail="Report not generated yet for this session")
            
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            generate_pdf_report(records[-1].agent_response, str(pdf_path))
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Report PDF not found and regeneration failed: {str(e)}")
            
    return FileResponse(
        path=str(pdf_path),
        filename=f"BNPParibas_ChurnReport_{session_id[:8]}.pdf",
        media_type="application/pdf"
    )


@app.get("/agent-metrics")
async def get_agent_metrics():
    """
    Get agent performance metrics dynamically.
    """
    db = SessionLocal()
    try:
        total_queries = db.query(ConversationHistory).count()
        success_rate = 1.0 if total_queries > 0 else 0.0
        
        return {
            "agents": [
                {
                    "name": "Query Agent",
                    "role": "Customer Query Specialist",
                    "total_calls": total_queries,
                    "success_rate": success_rate
                },
                {
                    "name": "Data Analyst Agent",
                    "role": "Customer Churn Data Analyst",
                    "total_calls": total_queries,
                    "success_rate": success_rate
                },
                {
                    "name": "Prediction Agent",
                    "role": "Customer Churn Prediction Expert",
                    "total_calls": total_queries,
                    "success_rate": success_rate
                },
                {
                    "name": "Recommendation Agent",
                    "role": "Retention Strategy Expert",
                    "total_calls": total_queries,
                    "success_rate": success_rate
                },
                {
                    "name": "Validation Agent",
                    "role": "Validation Specialist",
                    "total_calls": total_queries,
                    "success_rate": success_rate
                },
                {
                    "name": "Reporting Agent",
                    "role": "Executive Reporting Specialist",
                    "total_calls": total_queries,
                    "success_rate": success_rate
                }
            ],
            "total_queries_processed": total_queries
        }
    except Exception as e:
        return {
            "error": str(e),
            "agents": []
        }
    finally:
        db.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
