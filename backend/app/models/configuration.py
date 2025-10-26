from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Configuration(Base):
    """
    Configuration model for storing dynamic settings
    All API keys, prompts, and configuration values are stored here
    """
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=True)
    group = Column(String(50), nullable=True)  # For grouping in admin UI
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Configuration(key={self.key}, group={self.group})>"