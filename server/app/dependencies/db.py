from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.db.session import get_session


def get_db():
    yield from get_session()


DBSession = Annotated[Session, Depends(get_db)]
