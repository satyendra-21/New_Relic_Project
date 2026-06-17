from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime
from log_fetcher.utils.exceptions import ValidationException


class SnapshotRequest(BaseModel):
    service_name: str
    start_time: str
    end_time: str
    trace_id: Optional[str] = None

    @model_validator(mode='after')
    def check_time_window(self) -> 'SnapshotRequest':
        try:
            start = datetime.fromisoformat(self.start_time.replace('Z', '+00:00'))
            end = datetime.fromisoformat(self.end_time.replace('Z', '+00:00'))
            if start >= end:
                raise ValidationException(f"start_time ({self.start_time}) must be strictly before end_time ({self.end_time})")
        except ValueError as e:
            if not isinstance(e, ValidationException):
                raise ValidationException("Invalid datetime format. Please use ISO 8601 (e.g., 2026-05-19T10:00:00)")
            raise e
        return self