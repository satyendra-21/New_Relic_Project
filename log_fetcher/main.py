from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
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
from log_fetcher.utils.exceptions import (
    ValidationException, AuthenticationException, UpstreamAPIException, LogsNotFoundException
)

app = FastAPI()

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(status_code=400, content={"error": "ValidationException", "message": str(exc)})

@app.exception_handler(AuthenticationException)
async def auth_exception_handler(request: Request, exc: AuthenticationException):
    return JSONResponse(status_code=401, content={"error": "AuthenticationException", "message": str(exc)})

@app.exception_handler(UpstreamAPIException)
async def upstream_exception_handler(request: Request, exc: UpstreamAPIException):
    return JSONResponse(status_code=502, content={"error": "UpstreamAPIException", "message": str(exc)})

@app.exception_handler(LogsNotFoundException)
async def not_found_exception_handler(request: Request, exc: LogsNotFoundException):
    return JSONResponse(status_code=404, content={"error": "LogsNotFoundException", "message": str(exc)})

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