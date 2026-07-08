from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    pass