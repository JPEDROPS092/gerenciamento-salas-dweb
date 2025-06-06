from app.models import db
from app.models import dto


def db_to_get_dto(user_db: db.UserDb) -> dto.UserDTO:
    """Convert a User DB object to a GetUser DTO"""
    return dto.UserDTO(
        id=user_db.id,
        name=user_db.name,
        surname=user_db.surname,
        role=user_db.role,
        email=user_db.email,
        updated_at=user_db.updated_at,
        created_at=user_db.created_at
    )