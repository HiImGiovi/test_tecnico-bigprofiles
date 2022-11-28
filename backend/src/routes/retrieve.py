from fastapi import FastAPI, APIRouter, Query, Depends
from fastapi.security.api_key import APIKey

from src.auth import get_api_key

from src.models import ResultModel
from src.db import enrich_inputs_collection

import datetime

router = APIRouter(
    prefix="/retrieve",
)


@router.get("",
            tags=["retrieve"],
            operation_id="retrieve_api_v1_retrieve_get",
            response_model=ResultModel,
            description="Endpoint che permette di andare ad estrarre i valori aggregati per minuto. <br />La risposta contiene la lista dei valori aggregati per minuto con le varie informazioni necessarire; inoltre vengono mandati gli ultimi 10 log in ordine temporale inverso (dal più recente al meno) dell'ultima aggregazione della selezione scelta.<br />E' possibile andare a cambiare il range temporale scelto.<br />",
            responses={
                200: {"model": ResultModel, "description": "Response",
                      "example": {
                        "values":
                        [
                            {
                                            "key": 1,
                                            "creation_datetime": "2021-07-18T10:40:00",
                                            "total_response_time_ms": 1234,
                                            "total_requests": 20,
                                            "total_errors": 2
                            },
                            {
                                "key": 2,
                                "creation_datetime": "2021-07-18T10:41:00",
                                "total_response_time_ms": 44,
                                "total_requests": 2,
                                "total_errors": 0
                            },
                            {
                                "key": 3,
                                "creation_datetime": "2021-07-18T10:41:00",
                                "total_response_time_ms": 24,
                                "total_requests": 2,
                                "total_errors": 0
                            }
                        ],
                          "logs":
                          [
                            {
                                "key": 3,
                                "payload": "Stringa di prova",
                                "creation_datetime": "2021-07-18T10:41:45",
                                "response_time": 14,
                                "response_code": 200
                            },
                            {
                                "key": 2,
                                "payload": "Stringa di prova",
                                "creation_datetime": "2021-07-18T10:41:34",
                                "response_time": 24,
                                "response_code": 200
                            },
                            {
                                "key": 3,
                                "payload": "Stringa di prova",
                                "creation_datetime": "2021-07-18T10:41:24",
                                "response_time": 10,
                                "response_code": 200
                            },
                            {
                                "key": 2,
                                "payload": "Stringa di prova",
                                "creation_datetime": "2021-07-18T10:41:10",
                                "response_time": 20,
                                "response_code": 200
                            }
                        ]
                      }}
            })
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
        example="2021-07-28 13:50:00.000Z"),
    api_key: APIKey = Depends(get_api_key)
):
    date_from_dt = datetime.datetime.fromisoformat(date_from.replace("Z", ""))
    date_to_dt = datetime.datetime.fromisoformat(date_to.replace("Z", ""))

    # rounding date to next minute
    date_to_dt += datetime.timedelta(minutes=1)
    date_to_dt = date_to_dt.replace(second=0, microsecond=0)
    values = list(enrich_inputs_collection.aggregate(
        [
            {
                "$match": {"creation_datetime": {"$gte": date_from_dt, "$lte": date_to_dt}},
            },
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
            },
        ],
        # "logs": [
        #     {
        #         "$sort": {"creation_datetime": -1}
        #     },
        #     {
        #         "$limit": 10
        #     },
        #     {
        #         "$project": {
        #             "_id": 0,
        #             "key": "$key",
        #             "payload": "$payload",
        #             "response_time": "$response_time",
        #             "response_code": "$response_code",
        #             "creation_datetime": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S.%L", "date": "$creation_datetime"}},
        #         }
        #     }
        # ]


    ))
    if (len(values) > 0):

        last_agg_datetime_from = datetime.datetime.fromisoformat(
            values[len(values) - 1]["creation_datetime"])
        last_agg_datetime_to = last_agg_datetime_from + \
            datetime.timedelta(minutes=1)

        logs = list(enrich_inputs_collection.aggregate(
            [
                {
                    "$match": {"creation_datetime": {"$gte": last_agg_datetime_from, "$lt": last_agg_datetime_to}},
                },
                {
                    "$sort": {"creation_datetime": -1}
                },
                {
                    "$limit": 10
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
            ]))
    else:
        logs = []

    return {
        "values": values,
        "logs": logs
    }
