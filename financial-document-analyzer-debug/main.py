from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from redis import Redis
from rq import Queue

from crew_runner import run_crew
from db import init_db, store_analysis, get_analysis

app = FastAPI(title="Financial Document Analyzer")

# Initialize database and Redis queue on startup
init_db()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_conn = Redis.from_url(redis_url)
analysis_queue = Queue("financial_analysis", connection=redis_conn)


@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document"),
):
    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        response = run_crew(query=query.strip(), file_path=file_path)

        analysis_id = file_id
        store_analysis(
            analysis_id=analysis_id,
            file_name=file.filename,
            query=query.strip(),
            analysis=str(response),
        )

        return {
            "status": "success",
            "analysis_id": analysis_id,
            "analysis": str(response),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/analyze-async")
async def analyze_financial_document_async_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document"),
):
    """
    Enqueue a background job to analyze the uploaded financial document.

    Returns immediately with an analysis_id and job_id that can be used
    to retrieve the result later.
    """
    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        analysis_id = file_id

        job = analysis_queue.enqueue(
            "queue_tasks.analyze_financial_document_job",
            analysis_id,
            file_path,
            query.strip(),
            file.filename,
        )

        return {
            "status": "queued",
            "analysis_id": analysis_id,
            "job_id": job.id,
        }

    except Exception as e:
        # Clean up file if queuing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analysis/{analysis_id}")
async def get_analysis_endpoint(analysis_id: str):
    """
    Retrieve a previously stored analysis result.
    """
    record = get_analysis(analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "status": "success",
        "analysis": record,
    }
