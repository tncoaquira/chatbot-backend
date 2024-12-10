from starlette.responses import JSONResponse
from fastapi import HTTPException


def successResponse(data, status_code=200, message="Operacion realizada exitosamente"):
    # Asegúrate de que `data` sea serializable
    return JSONResponse(
        content={"datos": data, "mensaje": message},
        status_code=status_code,
    )


def errorResponse(detail, message="Error en el servidor", status_code=500):
    # Si `detail` es una excepción, extrae el mensaje de error
    if isinstance(detail, Exception):
        detail = str(detail)  # Convierte la excepción a cadena para serializarla
    return JSONResponse(
        content={"success": False, "message": message, "detail": detail},
        status_code=status_code,
    )
