from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Workspace(Base):
    __tablename__ = "workspaces"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(
        "User",
        back_populates = "workspaces"
    )