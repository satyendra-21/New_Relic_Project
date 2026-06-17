class LogFetcherException(Exception):
    """Base exception for the log fetcher service."""
    pass

class ValidationException(LogFetcherException):
    """Raised when request payload fails business validation."""
    pass

class AuthenticationException(LogFetcherException):
    """Raised when New Relic API authentication fails (401)."""
    pass

class UpstreamAPIException(LogFetcherException):
    """Raised when the New Relic API returns a server error (5xx) or timeout."""
    pass

class LogsNotFoundException(LogFetcherException):
    """Raised when no logs are found for the given criteria."""
    pass
