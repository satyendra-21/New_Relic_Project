def generate_snapshot(
    logs_response,
    request
):
    if not logs_response:
        return {
            "error": "No logs found"
        }
    raw_logs = (
        logs_response
        .get("data", {})
        .get("actor", {})
        .get("account", {})
        .get("nrql", {})
        .get("results", [])
    )

    parsed_logs = []

    severity_summary = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    for log in raw_logs:

        message = log.get("message", "")

        parts = message.split(" | ")

        if len(parts) < 3:
            continue

        timestamp = parts[0]
        level = parts[1]

        structured_log = {
            "timestamp": timestamp,
            "level": level
        }

        for item in parts[2:]:

            if "=" in item:

                key, value = item.split(
                    "=",
                    1
                )

                structured_log[
                    key.strip()
                ] = value.strip()

        if (
            request.trace_id
            and structured_log.get(
                "traceId"
            ) != request.trace_id
        ):
            continue

        parsed_logs.append(
            structured_log
        )

        if level in severity_summary:
            severity_summary[level] += 1

    snapshot = {
        "incident_window": {
            "start_time": request.start_time,
            "end_time": request.end_time
        },
        "service_name": request.service_name,
        "trace_id": request.trace_id,
        "log_count": len(parsed_logs),
        "severity_summary": severity_summary,
        "logs": parsed_logs
    }

    return snapshot