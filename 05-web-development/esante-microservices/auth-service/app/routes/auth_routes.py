from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Doctor
from app.schemas import (
    RegisterRequest, RegisterResponse,
    LoginRequest, TokenResponse,
    RefreshRequest, RefreshResponse,
)
from app.auth import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    verify_refresh_token,
)
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Endpoint 1 : Register ────────────────────────────────
@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Création d'un compte médecin",
)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """
    Crée un nouveau compte médecin.
    - Vérifie l'unicité de l'email
    - Hash le mot de passe avec bcrypt
    - Retourne le profil créé
    """
    existing = db.query(Doctor).filter(Doctor.email == body.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A doctor with this email already exists",
        )

    doctor = Doctor(
        email=body.email,
        password_hash=hash_password(body.password),
        first_name=body.first_name,
        last_name=body.last_name,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return RegisterResponse.model_validate(doctor)


# ── Endpoint 2 : Login ───────────────────────────────────
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authentification — obtention d'un token JWT",
)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Authentifie un médecin par email/password.
    Retourne un access_token (30 min) et un refresh_token (7 jours).
    """
    doctor = db.query(Doctor).filter(Doctor.email == body.email).first()
    if not doctor or not verify_password(body.password, doctor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return TokenResponse(
        access_token=create_access_token(doctor.id, doctor.email),
        refresh_token=create_refresh_token(doctor.id, doctor.email),
    )


# ── Endpoint 3 : Refresh ─────────────────────────────────
@router.post(
    "/refresh",
    response_model=RefreshResponse,
    summary="Rafraîchissement du token JWT",
)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    """
    Rafraîchit un access_token à partir d'un refresh_token valide.
    """
    try:
        payload = verify_refresh_token(body.refresh_token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    doctor = db.query(Doctor).filter(Doctor.id == int(payload["sub"])).first()
    if not doctor:
        raise HTTPException(status_code=401, detail="Doctor not found")

    return RefreshResponse(
        access_token=create_access_token(doctor.id, doctor.email)
    )
