from pydantic import BaseModel
from datetime import date
from typing import List


class FinancialDataBase(BaseModel):
    symbol: str
    date: date
    open_price: float
    close_price: float
    volume: int

# class FinancialData(BaseModel):
#     id: str
#     symbol: str
#     date: date
#     open_price: float
#     close_price: float
#     volume: int

#     class Config:
#         orm_mode = True

class FinancialData(FinancialDataBase):
    id: str

    class Config:
        orm_mode = True

# all the members are Strings to allow overriding the default error messages
class Pagination(BaseModel):
    count: str
    page: str
    limit: str
    pages: str

class Info(BaseModel):
    error: str

class RequestResultPaginated(BaseModel):
    data: List[FinancialData] 
    info: Info
    pagination: Pagination

class RequestResultPaginatedOut(BaseModel):
    data: List[FinancialDataBase]
    info: Info
    pagination: Pagination

class Statistics(BaseModel):
    start_date: date
    end_date: date
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: int

class StatisticsReport(BaseModel):
    data: Statistics | None = None
    info: Info