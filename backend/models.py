from sqlalchemy import Column, Integer, String, Float
from database import Base

class CurrencyRate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    currency = Column(String)
    mid = Column(Float)
