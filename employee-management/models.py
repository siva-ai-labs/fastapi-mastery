
from decimal import Decimal

from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
