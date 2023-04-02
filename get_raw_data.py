import asyncio
import httpx
import os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import OperationalError

postgresql_connection_string = os.environ.get('SQLALCHEMY_DATABASE_URL')
engine = create_engine(postgresql_connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Financial_Data(Base):
    __tablename__ = "financial_data"

    id = Column(String, primary_key=True, index=True)
    symbol = Column(String)
    date = Column(Date, default=None)
    open_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)

#persistent parameters
uri_string = "https://www.alphavantage.co/query"
function_name_string = "TIME_SERIES_DAILY_ADJUSTED"
api_key = os.environ.get('ALPHAVANTAGE_API_KEY')
weekdays_number = 10

#captions used by Alphavantage in their JSON response
time_series_caption_str = "Time Series (Daily)"
open_price_caption_str = "1. open"
close_price_caption_str = "4. close"
volume_caption_str = "6. volume"

async def getdata(db: SessionLocal):
    async with httpx.AsyncClient() as client:
        symbols = ["IBM", "AAPL"]
        headers = {'Accept': 'application/json'}
        
        for symbol in symbols:
            params = {'function': function_name_string,
                'symbol': symbol, 'apikey': api_key}
            response = await client.get(uri_string, headers=headers, params=params)
            #check response is successful
            if response.status_code != 200:
                raise ValueError(f"Error retrieving data for symbol {symbol}. HTTP status code {response.status_code}")
            
            response_data = response.json()
            daily_data = response_data.get(time_series_caption_str)
            #check daily_data is present
            if daily_data is None:
                raise ValueError(f"Error retrieving data for symbol {symbol}. JSON response does not contain '{time_series_caption_str}' key.")
            
            dates = list(daily_data.keys())[0:weekdays_number]
            datas = list(daily_data.values())[0:weekdays_number]

            #reformat the data to be displayed and stored in DB
            raw_values = []
            for date, data in zip(dates, datas):
                #check date is in proper format
                try:
                    dd = datetime.strptime(date, '%Y-%m-%d').date()
                except ValueError:
                    print(f"Error parsing date {date}")

                #check data is present
                if open_price_caption_str not in data or close_price_caption_str not in data or volume_caption_str not in data:
                    raise ValueError(f"Error retrieving data for symbol {symbol}. JSON response does not contain required captions.")
                open_price = data[open_price_caption_str]
                close_price = data[close_price_caption_str]
                volume = data[volume_caption_str]
                
                print("{\n\t'date': "+date+"\n\t'symbol': "+symbol+"\n\t'open_price': "+open_price+"\n\t'close_price': "+close_price+"\n\t'volume': "+volume+"\n},")

                raw_values.append({"id": symbol+date, "symbol": symbol, "date": dd,
                                "open_price": open_price, "close_price": close_price, "volume": volume})

            #save to DB avoiding duplicates
            stmt = insert(Financial_Data).values(raw_values)
            stmt = stmt.on_conflict_do_nothing(
                index_elements=['id']
            )
            #check queries execution
            try:
                db.execute(stmt)
                db.commit()
            except Exception as e:
                print(f"Error storing data in database: {e}")

        return

try:
    data = getdata(db=SessionLocal())
except OperationalError as e:
    raise type(e)(f"Error connecting to the database: {str(e)}")
except httpx.HTTPError as e:
    raise type(e)(f"Error making HTTP request to Alphavantage API: {str(e)}")

asyncio.run(data)