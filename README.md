# Genderize API Integration & Data Processing

## Overview

This project implements a simple REST API that integrates with the external Genderize API to classify a given name by gender.

The API processes the raw response from Genderize and returns a structured result with additional computed fields such as confidence level and timestamp.

---

## Base URL

```
https://your-deployed-url.com
```

---

## Endpoint

### GET /api/classify

#### Query Parameters

| Parameter | Type   | Required | Description          |
| --------- | ------ | -------- | -------------------- |
| name      | string | Yes      | The name to classify |

---

## Success Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```

---

## Error Responses

### 400 Bad Request

Returned when the `name` parameter is missing or empty.

```json
{
  "status": "error",
  "message": "Missing or empty name parameter"
}
```

---

### 422 Unprocessable Entity

Returned when:

* The query parameter type is invalid (handled automatically by FastAPI)
* No prediction is available from the Genderize API

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

---

### 502 Bad Gateway

Returned when the external Genderize API fails or is unavailable.

```json
{
  "status": "error",
  "message": "External API request failed"
}
```

---

## Processing Logic

The API performs the following steps:

1. Validates the input query parameter
2. Calls the Genderize API
3. Extracts relevant fields:

   * gender
   * probability
   * count (renamed to `sample_size`)
4. Computes:

   * `is_confident` = true if:

     * probability ≥ 0.7 AND sample_size ≥ 100
5. Generates:

   * `processed_at` (UTC, ISO 8601 format)

---

## Edge Case Handling

If the Genderize API returns:

* `gender = null` OR
* `count = 0`

The API responds with:

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```

---

## CORS Configuration

CORS is enabled to allow requests from any origin:

```
Access-Control-Allow-Origin: *
```

This ensures compatibility with external grading scripts.

---

## Tech Stack

* Python
* FastAPI
* httpx (for async HTTP requests)
* Uvicorn

---

## Running Locally

### 1. Clone the repository

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a virtual environment

```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the server

```
uvicorn main:api --reload
```

### 5. Test the endpoint

```
http://127.0.0.1:8000/api/classify?name=john
```

---

## Notes

* The API is designed to handle multiple concurrent requests using asynchronous HTTP calls.
* FastAPI automatically validates query parameter types and returns appropriate 422 errors when invalid input is provided.
* External API calls include timeout handling to prevent hanging requests.

---

## Author

Richard Ezea
[your.email@example.com](mailto:rclancing@gmail.com)
