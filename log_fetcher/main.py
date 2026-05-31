from fastapi import FastAPI, HTTPException
from log_fetcher.services.snapshot_service import (
    generate_snapshot
)
from log_fetcher.models.snapshot import (
    SnapshotRequest
)

from log_fetcher.services.newrelic_service import (
    fetch_logs
)
from log_fetcher.utils.logger import (
    logger
)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "New Relic Log Fetcher Running"
    }


@app.post("/snapshot")
def create_snapshot(
    request: SnapshotRequest
):

    logger.info(
        "Snapshot request started"
    )

    try:

        logs = fetch_logs(
            service_name=request.service_name,
            start_time=request.start_time,
            end_time=request.end_time,
            trace_id=request.trace_id
        )

        logger.info(
            "Logs fetched successfully"
        )

        snapshot = generate_snapshot(
            logs,
            request
        )

        logger.info(
            "Snapshot generated successfully"
        )

        return snapshot

    except Exception as e:

        logger.error(
            f"Snapshot generation failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )