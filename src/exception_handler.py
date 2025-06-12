from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app import app


@app.exception_handler(HTTPException)
def handle_bad_request_exception(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"{exc.__class__.__name__}",
            "message": exc.detail,
            "metadata": {
                "request_info": {"url": str(request.url), "method": request.method},
                "request_headers": {
                    header[0]: header[1] for header in request.headers.items()
                },
            },
        },
    )
