from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from queries import daily_sales, top_customers, sales_by_city

app = FastAPI()


@app.get("/sales/daily", response_class=PlainTextResponse)
async def get_daily_sales(date1: str, date2: str = None):
    return await daily_sales(date1, date2)


@app.get("/customers/top", response_class=PlainTextResponse)
async def get_top_customers():
    return await top_customers()


@app.get("/sales/city", response_class=PlainTextResponse)
async def get_sales_city():
    return await sales_by_city()