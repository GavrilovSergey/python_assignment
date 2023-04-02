from sqlalchemy import Column, Integer, Float, String, Date
from .database import Base

#stores daily finincial data of a given stock
class Financial_Data(Base):
    __tablename__ = "financial_data"

    id = Column(String, primary_key=True, index=True)
    symbol = Column(String)
    date = Column(Date, default=None)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)