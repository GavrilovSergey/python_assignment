import math
from sqlalchemy import asc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import FastAPI, Depends
from . import helpers, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def getFinancialData(db: Session, start_date, end_date, symbol, page, limit):
    if symbol is not None:
        count = db.query(models.Financial_Data).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).filter(models.Financial_Data.symbol == symbol).count()
        data = db.query(models.Financial_Data).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).filter(models.Financial_Data.symbol == symbol).order_by(asc(models.Financial_Data.date)).offset((page-1)*limit).limit(limit).all()
    else:
        count = db.query(models.Financial_Data).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).count()
        data = db.query(models.Financial_Data).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).order_by(asc(models.Financial_Data.date)).offset((page-1)*limit).limit(limit).all()

    return schemas.RequestResultPaginated(data=data, pagination = {"count": count, "page": page, "limit": limit, "pages": math.ceil(count/limit)}, info = {"error": ""})

@app.get("/api/financial_data", response_model=schemas.RequestResultPaginatedOut)
async def get_financial_data(start_date: str | None = None, end_date: str | None = None, symbol: str | None = None, page: str = "1", limit: str = "5", db: Session = Depends(get_db)):
    '''get the requested financial data'''
    #fast-fail checks for the cases of inapropriate request parameters
    start_date, end_date, info = helpers.validateDates(start_date, end_date)
    if start_date is None or end_date is None:
        return schemas.RequestResultPaginated(data = [], pagination = {"count": 0, "page": page, "limit": limit, "pages": 0}, info = info) 
    
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        return schemas.RequestResultPaginated(data=[], pagination = {"count": 0, "page": page, "limit": limit, "pages": 0}, info={"error": "Invalid page or limit"})

    if page < 1 or limit < 1:
        return schemas.RequestResultPaginated(data=[], pagination = {"count": 0, "page": page, "limit": limit, "pages": 0}, info={"error": "Invalid page or limit"})

    #all fast-fail checks passed, proceed to query
    data = getFinancialData(
        db, start_date=start_date, end_date=end_date, symbol=symbol, page=page, limit=limit)
    return data


def getStatisticsData(db: Session, start_date, end_date, symbol):
    #evaluate statistics
    average_daily_open_price = db.query(func.avg(models.Financial_Data.open_price).label("average_daily_open_price")).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).filter(models.Financial_Data.symbol == symbol).scalar()
    average_daily_close_price = db.query(func.avg(models.Financial_Data.close_price).label("average_daily_close_price")).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).filter(models.Financial_Data.symbol == symbol).scalar()
    average_daily_volume = db.query(func.avg(models.Financial_Data.volume).label("average_daily_volume")).filter(models.Financial_Data.date >= start_date).filter(models.Financial_Data.date <= end_date).filter(models.Financial_Data.symbol == symbol).scalar()

    if average_daily_open_price is None or average_daily_open_price is None or average_daily_volume is None:
        return schemas.StatisticsReport(data=None, info = {"error": "statistic evaluation failed. Possibly wrong [symbol] parameter or data is mising."})
    data = {"start_date": start_date, "end_date": end_date, "symbol": symbol, "average_daily_open_price": round(average_daily_open_price, 2), "average_daily_close_price": round(average_daily_close_price, 2), "average_daily_volume": average_daily_volume}
    return schemas.StatisticsReport(data=data, info = {"error": ""})
    
@app.get("/api/statistics", response_model=schemas.StatisticsReport)
async def get_statistics_data(start_date: str, end_date: str, symbol: str, db: Session = Depends(get_db)):
    '''get the statistics for a specified period'''
    #fast-fail checks for the cases of inapropriate request parameters
    start_date, end_date, info = helpers.validateDates(start_date, end_date)
    if start_date is None or end_date is None:
        return schemas.StatisticsReport(data = None, info = info) 
    
    #all fast-fail checks passed, proceed to query
    data = getStatisticsData(
        db, start_date=start_date, end_date=end_date, symbol=symbol)
    return data