from fastapi.responses import JSONResponse, Response


def badresponse(message: str = "Invalid request", code: int = 400):
    return JSONResponse(content={"message": message, "status": "error"}, status_code=code)


def okresponse(message: str = "success", code: int = 200):
    return JSONResponse(content={"message": message, "status": "success"}, status_code=code)


def emptyresponse(code: int = 204):
    return Response(status_code=code)
