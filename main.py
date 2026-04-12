import re
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


@api.get("/api/classify", status_code=200)
async def main(name: str = None):
    # Check that input exists
    if not name or not name.strip():
        return JSONResponse(
            status_code=400,
            content={
                "status":
                    "error",
                "message":
                    "Missing or empty name parameter"
            })

    # Check that input is a String
    if not re.fullmatch(r"^[A-Za-z]+([ '-][A-Za-z]+)*$", name):
        return JSONResponse(
            status_code=422,
            content={
                "status":
                    "error",
                "message":
                    "Name contains invalid characters"
            }
        )

    # Call genderize API
    result, error = await get_gender_api(name)

    if error:
        return JSONResponse(**error)

    return JSONResponse(
        status_code=200,
        content=process_response(result)
    )


async def get_gender_api(name):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url=f"https://api.genderize.io?name={name}",
                timeout=5
            )
    except httpx.RequestError:
        # Handle failed request from API call
        return None, {
            "status_code": 502,
            "content": {
                "status": "error",
                "message": "External API request failed"
            }
        }

    # Handle invalid response from API call
    if r.status_code != 200:
        return None, {
            "status_code": 502,
            "content": {
                "status": "error",
                "message": "Invalid response from external API"
            }
        }

    result = r.json()

    # Test for edge case
    if result["gender"] is None or result["count"] == 0:
        return None, {
            "status_code": 422,
            "content": {
                "status": "error",
                "message":
                    "No prediction available for the provided name"
            }
        }

    return result, None


def process_response(result):
    response = {
        "status": "success",
        "data": {
            "name": result.get("name"),
            "gender": result.get("gender"),
            "probability": result.get("probability"),
            "sample_size": result.get("count"),
            "is_confident":
                result.get("probability") >= 0.7 and
                result.get("count") >= 100,
            "processed_at":
                datetime.now(timezone.utc)
                .isoformat(timespec='seconds')
                .replace('+00:00', 'Z')
        }
    }
    return response
