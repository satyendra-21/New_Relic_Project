from pydantic import BaseModel
from typing import Optional


class SnapshotRequest(BaseModel):
    service_name: str
    start_time: str
    end_time: str
    trace_id: Optional[str] = None