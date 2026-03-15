from fastapi import Request
from fastapi.responses import JSONResponse


# ── Base ──────────────────────────────────────────────────────────────────────


class AppError(Exception):
    """Base class for all application-level errors."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# ── Concrete errors ───────────────────────────────────────────────────────────


class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            f"{resource} '{identifier}' not found",
            status_code=404,
        )


class UnauthorizedError(AppError):
    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(detail, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(detail, status_code=403)


class ConflictError(AppError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            f"{resource} '{identifier}' already exists",
            status_code=409,
        )


class RateLimitError(AppError):
    def __init__(self, retry_after: int) -> None:
        super().__init__(
            f"Rate limit exceeded. Try again in {retry_after} seconds.",
            status_code=429,
        )
        self.retry_after = retry_after


class ExternalServiceError(AppError):
    def __init__(self, service: str, detail: str = "") -> None:
        msg = f"External service '{service}' error"
        if detail:
            msg = f"{msg}: {detail}"
        super().__init__(msg, status_code=502)


class AIDisabledError(AppError):
    def __init__(self) -> None:
        super().__init__(
            "AI features are currently disabled. Please try again later.",
            status_code=503,
        )


# ── FastAPI exception handlers ────────────────────────────────────────────────


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    headers: dict[str, str] = {}
    if isinstance(exc, RateLimitError):
        headers["Retry-After"] = str(exc.retry_after)
    return JSONResponse(
        status_code=exc.status_code,
        content={"data": None, "error": exc.message, "meta": None},
        headers=headers,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    import structlog

    logger = structlog.get_logger()
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"data": None, "error": "An unexpected error occurred.", "meta": None},
    )
