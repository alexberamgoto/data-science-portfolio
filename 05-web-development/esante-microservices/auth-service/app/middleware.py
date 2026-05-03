from fastapi import Request, HTTPException
from app.auth import verify_access_token
from jose import JWTError


async def get_current_doctor(request: Request) -> dict:
    """
    Extract and validate the JWT access token from the Authorization header.
    Returns dict with doctor_id and email.
    """
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )

    token = authorization.split(" ")[1]

    try:
        payload = verify_access_token(token)
        return {
            "doctor_id": int(payload["sub"]),
            "email": payload["email"],
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
