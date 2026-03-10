from database import orders_collection
from tabulate import tabulate


async def daily_sales(date1: str, date2: str = None):

    if date2:
        match_stage = {
            "$match": {
                "order_date": {
                    "$gte": f"{date1}T00:00:00Z",
                    "$lte": f"{date2}T23:59:59Z"
                }
            }
        }
    else:
        match_stage = {
            "$match": {"order_date": {"$regex": f"^{date1}"}}
        }

    pipeline = [
        match_stage,
        {
            "$group": {
                "_id": {"$substr": ["$order_date", 0, 10]},
                "total_sales": {"$sum": "$total_amount"},
                "orders_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": -1}}
    ]

    result = list(orders_collection.aggregate(pipeline))

    table_data = []

    for r in result:
        table_data.append([
            r["_id"],
            f"${r['total_sales']:.2f}",
            r["orders_count"]
        ])

    table = tabulate(
        table_data,
        headers=["Date", "Total Sales", "Orders Count"],
        tablefmt="grid"
    )

    return table
async def top_customers():

    pipeline = [
        {
            "$group": {
                "_id": "$customer_id",
                "total_spent": {"$sum": "$total_amount"},
                "orders": {"$sum": 1},
                "last_order": {"$max": "$order_date"}
            }
        },
        {"$sort": {"total_spent": -1}},
        {"$limit": 5}
    ]

    result = list(orders_collection.aggregate(pipeline))

    table_data = []

    for r in result:
        table_data.append([
            r["_id"],
            f"${r['total_spent']:.2f}",
            r["orders"],
            r["last_order"]
        ])

    table = tabulate(
        table_data,
        headers=["Customer", "Total Spent", "Orders", "Last Order"],
        tablefmt="grid"
    )

    return {"table": table}
async def sales_by_city():

    pipeline = [
        {
            "$group": {
                "_id": "$city",
                "total_sales": {"$sum": "$total_amount"},
                "orders": {"$sum": 1},
                "avg_order": {"$avg": "$total_amount"}
            }
        },
        {"$sort": {"total_sales": -1}},
        {"$limit": 20}
    ]

    result = list(orders_collection.aggregate(pipeline))

    table_data = []

    for r in result:
        table_data.append([
            r["_id"],
            f"${r['total_sales']:.2f}",
            r["orders"],
            f"${r['avg_order']:.2f}"
        ])

    table = tabulate(
        table_data,
        headers=["City", "Total Sales", "Orders", "Avg Order"],
        tablefmt="grid"
    )

    return {"table": table}