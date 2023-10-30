from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import carts, catalog
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
Customer PC Builder and Trader. Create templates, buy and sell PC parts for all your needs.
"""

app = FastAPI(
    title="Custom PC Builder and Trader",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Dillon Murphy, Sam Bock, Adam Del Rio, Nick Patrick",
        "email": "ddmurphy@calpoly.edu, sambock@email.com, adddelrio@email.com, nickpatrick@email.com",
    },

)

# origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(carts.router)
app.include_router(catalog.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Custom PC Builder and Trader."}
