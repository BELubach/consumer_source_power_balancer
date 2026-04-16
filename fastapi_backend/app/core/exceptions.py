from typing import cast
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class InvalidCredentials(Exception):
    def __init__(self, message: str):
        self.message = message

class ObjectAlreadyExists(Exception):
    def __init__(self, type: str, name: str):
        self.message = f"{type} with name '{name}' already exists"

class ResourceNotFoundException(Exception):
    def __init__(self, type: str, identifier: str):
        self.message = f"{type} with identifier '{identifier}' not found"


async def invalid_credentials_exception_handler(request: Request, exception: Exception):
    exc = cast(InvalidCredentials, exception)
    return JSONResponse(
        status_code=401,
        content={"message": exc.message},
    )

async def object_already_exists_exception_handler(request: Request, exception: Exception):
    exc = cast(ObjectAlreadyExists, exception)
    return JSONResponse(
        status_code=409,
        content={"message": exc.message},
    )

async def resource_not_found_exception_handler(request: Request, exception: Exception):
    exc = cast(ResourceNotFoundException, exception)
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidCredentials, invalid_credentials_exception_handler)
    app.add_exception_handler(ObjectAlreadyExists, object_already_exists_exception_handler)
    app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
