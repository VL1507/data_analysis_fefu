import datetime

from sqlalchemy import (
    DateTime,
    Double,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ActivityTypes(Base):
    __tablename__ = "activity_types"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="activity_types_pkey"),
        Index("activity_types_index_0", "type_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_name: Mapped[str] = mapped_column(String(255), nullable=False)

    fitness_data: Mapped[list["FitnessData"]] = relationship(
        "FitnessData", back_populates="activity_type"
    )


class FitnessData(Base):
    __tablename__ = "fitness_data"
    __table_args__ = (
        ForeignKeyConstraint(
            ["activity_type_id"],
            ["activity_types.id"],
            name="fitness_data_activity_type_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="fitness_data_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recorded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(True), nullable=False, server_default=text("now()")
    )
    activity_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    steps: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_km: Mapped[float] = mapped_column(Double(53), nullable=False)
    kilocalories: Mapped[float] = mapped_column(Double(53), nullable=False)
    lat: Mapped[float] = mapped_column(Double(53), nullable=False)
    lon: Mapped[float] = mapped_column(Double(53), nullable=False)

    activity_type: Mapped["ActivityTypes"] = relationship(
        "ActivityTypes", back_populates="fitness_data"
    )
