from fastapi import APIRouter, Query

from src.models import ResultModel
from src.db import conn
import datetime
router = APIRouter(
    prefix="/retrieve",
)


@router.get("",
            tags=["retrieve"],
            operation_id="retrieve_api_v1_retrieve_get",
            response_model=ResultModel)
def retrieve(
    date_from: str = Query(
        None,
        title="Date from",
        description="Data di inizio della finestra temporale scelta, deve essere in formato ISO",
        format="date-time",
        example="2021-07-28 13:25:00.000Z"),
    date_to: str = Query(
        None,
        title="Date to",
        description="Data di fine della finestra temporale scelta, deve essere in formato ISO",
        format="date-time",
        example="2021-07-28 13:50:00.000Z")
    # api_key: APIKey = Depends(get_api_key)
):
    print(date_from)
    date_from_dt = datetime.datetime.fromisoformat(date_from.replace("Z", ""))
    date_to_dt = datetime.datetime.fromisoformat(date_to.replace("Z", ""))

    # rounding date to next minute
    date_to_dt += datetime.timedelta(minutes=1)
    date_to_dt = date_to_dt.replace(second=0, microsecond=0)
    outputs = list(conn.local.enrich_inputs.aggregate(
        [
            {
                "$match": {"creation_datetime": {"$gte": date_from_dt, "$lte": date_to_dt}},
            },
            {
                "$facet": {
                    "values": [
                        {
                            "$group": {
                                "_id": {
                                    "key": "$key",
                                    "creation_year": {"$year": "$creation_datetime"},
                                    "creation_month": {"$month": "$creation_datetime"},
                                    "creation_day": {"$dayOfMonth": "$creation_datetime"},
                                    "creation_hour": {"$hour": "$creation_datetime"},
                                    "creation_min": {"$minute": "$creation_datetime"},
                                },
                                "total_requests": {"$sum": 1},
                                "total_errors": {"$sum": {"$cond": [{"$eq": ['$response_code', 500]}, 1, 0]}},
                                "total_response_time_ms": {"$sum": "$response_time"}
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "key": "$_id.key",
                                "total_response_time_ms": "$total_response_time_ms",
                                "total_requests": "$total_requests",
                                "total_errors": "$total_errors",
                                "creation_datetime": {
                                    "$concat": [
                                        {"$toString": "$_id.creation_year"},
                                        "-",
                                        {
                                            "$cond": [
                                                {"$gt": [
                                                    "$_id.creation_month", 9]},
                                                {"$toString": "$_id.creation_month"},
                                                {"$concat": [
                                                    "0",
                                                    {"$toString": "$_id.creation_month"}
                                                ]}
                                            ]
                                        },
                                        "-",
                                        {
                                            "$cond": [
                                                {"$gt": [
                                                    "$_id.creation_day", 9]},
                                                {"$toString": "$_id.creation_day"},
                                                {"$concat": [
                                                    "0",
                                                    {"$toString": "$_id.creation_day"}
                                                ]}
                                            ]
                                        },
                                        " ",
                                        {
                                            "$cond": [
                                                {"$gt": [
                                                    "$_id.creation_hour", 9]},
                                                {"$toString": "$_id.creation_hour"},
                                                {"$concat": [
                                                    "0",
                                                    {"$toString": "$_id.creation_hour"}
                                                ]}
                                            ]
                                        },
                                        ":",
                                        {
                                            "$cond": [
                                                {"$gt": [
                                                    "$_id.creation_min", 9]},
                                                {"$toString": "$_id.creation_min"},
                                                {"$concat": [
                                                    "0",
                                                    {"$toString": "$_id.creation_min"}
                                                ]}
                                            ]
                                        },
                                        ":00",
                                    ]
                                }

                            }
                        },
                        {
                            "$sort": {"creation_datetime": 1, "key": 1}
                        }],
                    "logs": [
                        {
                            "$sort": {"creation_datetime": -1}
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "key": "$key",
                                "payload": "$payload",
                                "response_time": "$response_time",
                                "response_code": "$response_code",
                                "creation_datetime": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S.%L", "date": "$creation_datetime"}},
                            }
                        }
                    ]
                }
            }

        ]
    ))

    return {
        "values": outputs[0]["values"],
        "logs": outputs[0]["logs"][0:10]
    }
