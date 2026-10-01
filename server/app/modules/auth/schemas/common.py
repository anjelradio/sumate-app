from sqlmodel import SQLModel


class UserRead(SQLModel):
    """Public user data returned by auth endpoints."""
    # id ? uuid
    first_name: str
    last_name: str
    email: str
    is_super_admin: bool
    model_config = {"from_attributes": True}
