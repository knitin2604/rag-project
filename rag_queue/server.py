from fastapi import FastAPI, Query
from clients.rq_client import queue
from queues.worker import process_query
from rq.job import Job
from redis import Redis

app = FastAPI()

# Redis connection (needed to fetch job)
redis_conn = Redis(host="localhost", port=6379)


@app.get("/")
def root():
    return {"status": "Server is up and running"}


# ✅ enqueue job
@app.post("/chat")
def chat(
    query: str = Query(..., description="The chat query of user")
):
    job = queue.enqueue(process_query, query)

    return {
        "status": "queued",
        "job_id": job.id
    }


# ✅ check job result
@app.get("/job-status")
def get_results(
    job_id: str = Query(..., description="Job ID")
):
    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return {"status": "completed", "result": job.result}

    elif job.is_failed:
        return {"status": "failed"}

    else:
        return {"status": "in-progress"}