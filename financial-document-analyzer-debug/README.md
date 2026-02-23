# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents.

## Getting Started

### Install Required Libraries
```sh
pip install -r requirements.txt
```

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

**Note:** Current `data/sample.pdf` is a placeholder - replace with actual Tesla financial document for proper testing.

# You're Not All Set Yet!
🐛 **Debug Mode Activated!** The project originally shipped with intentional bugs - your mission is to fix them and bring it to life.

## Running the API

1. Make sure you have your OpenAI API key set:
   - Set `OPENAI_API_KEY` in a `.env` file or your environment.
2. Start the FastAPI server (from the project root where `main.py` lives):
   ```sh
   uvicorn main:app --reload
   ```
3. Open the interactive docs:
   - Navigate to `http://127.0.0.1:8000/docs` in your browser.

### `/analyze` Endpoint

- **Method**: `POST`
- **Path**: `/analyze`
- **Form fields**:
  - `file`: PDF file upload (the financial document to analyze)
  - `query` (optional): text question about the document  
    - Default: `"Analyze this financial document"`
- **Response** (on success):
  ```json
  {
    "status": "success",
    "analysis_id": "<id you can use to fetch later>",
    "analysis": "<model-generated structured analysis>"
  }
  ```

### `/analyze-async` Endpoint (Queue Worker)

- **Method**: `POST`
- **Path**: `/analyze-async`
- **Form fields**:
  - `file`: PDF file upload
  - `query` (optional): text question about the document
- **Behavior**:
  - Saves the file.
  - Enqueues a background job on a Redis-backed RQ queue (`financial_analysis`).
  - Returns immediately with:
    ```json
    {
      "status": "queued",
      "analysis_id": "<analysis id>",
      "job_id": "<rq job id>"
    }
    ```

### `/analysis/{analysis_id}` Endpoint

- **Method**: `GET`
- **Path**: `/analysis/{analysis_id}`
- **Description**: Fetch a stored analysis result by its `analysis_id`.
- **Response** (on success):
  ```json
  {
    "status": "success",
    "analysis": {
      "id": "<analysis id>",
      "file_name": "<original file name>",
      "query": "<original query>",
      "analysis": "<full analysis text>",
      "created_at": "<UTC ISO timestamp>"
    }
  }
  ```

## Bugs Fixed (Summary)

- **Incorrect install command**: `requirement.txt` ➝ `requirements.txt`.
- **Crew kickoff inputs**: Fixed `Crew.kickoff` to use `inputs={...}` so CrewAI receives `query` and `file_path` correctly.
- **PDF path handling**: Updated `FinancialDocumentTool.read_data_tool` to accept a dynamic `path` (defaulting to `data/sample.pdf`) and improved error messages.
- **Tool import**: Updated `SerperDevTool` import to the stable `from crewai_tools import SerperDevTool`.
- **Prompt and task design**:
  - Strengthened the financial analyst agent goal to avoid hallucinations and to rely on document content and tools.
  - Updated the analysis task description to:  
    - Explicitly reference `{file_path}` and `{query}`.  
    - Require calling `read_data_tool(path={file_path})` before analysis.  
    - Emphasize evidence-based metrics and clear educational (not advisory) framing.
 - **Queue worker model**:
   - Added an RQ-based background worker (`worker.py`) that listens on the `financial_analysis` queue and runs analyses concurrently.
   - Introduced an async API endpoint (`/analyze-async`) that enqueues jobs instead of blocking the request.
 - **Database integration**:
   - Introduced a lightweight SQLite-backed storage layer (`db.py`) that persists each analysis (id, file name, query, analysis text, timestamp).
   - Exposed a retrieval endpoint (`/analysis/{analysis_id}`) to fetch stored results.

## Running the Queue Worker and Database

The database is SQLite and is created automatically as `analysis_results.db` in the project root.

To use the async queue:

1. **Start Redis**
   - Ensure a Redis instance is running (for example via Docker):  
     ```sh
     docker run -p 6379:6379 redis
     ```
2. **Set the Redis URL (optional)**
   - By default the code uses `REDIS_URL=redis://localhost:6379/0`.
   - Override if needed in your environment.
3. **Start the RQ worker**
   - From the project root:
     ```sh
     rq worker financial_analysis
     ```
   - Or explicitly with `REDIS_URL`:
     ```sh
     REDIS_URL=redis://localhost:6379/0 rq worker financial_analysis
     ```
4. **Call `/analyze-async`**
   - Use the FastAPI docs at `http://127.0.0.1:8000/docs` to enqueue jobs.
   - Poll `/analysis/{analysis_id}` to retrieve the final stored result.

## Debugging Instructions

1. **Identify the Bug**: Carefully read the code in each file and understand the expected behavior. There is a bug in each line of code. So be careful.
2. **Fix the Bug**: Implement the necessary changes to fix the bug.
3. **Test the Fix**: Run the project and verify that the bug is resolved.
4. **Repeat**: Continue this process until all bugs are fixed.

## Expected Features
- Upload financial documents (PDF format)
- AI-powered financial analysis
- Investment recommendations
- Risk assessment
- Market insights
