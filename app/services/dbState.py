from app.models.dbState import DBState as DBStateDB
from app.models.country import Country
from typing import Literal, List, Union
from app.utils.time import datetime_utc_format, Datetime_Format, timestamp_utc_ms
from beanie import Link

TIME_SEG = Literal["DAY", "HOUR", "MIN"]
Links = List[Union[Link[Country]]]
DBStateActions = Literal["modify", "add", "delete"]
DBTables = Literal["nation"]

__all__ = ("updateDBState",)


def get_version() -> str:
    yymmdd = datetime_utc_format(Datetime_Format.YYYYMMDD)
    hhmmss = datetime_utc_format(Datetime_Format.HHMMSS)

    return f"{yymmdd}-{hhmmss}"


async def get_latest_dbstate(time_seg: TIME_SEG) -> Union[DBStateDB, None]:
    dbstate = (
        await DBStateDB.find(DBStateDB.time_seg == time_seg)
        .sort(-DBStateDB.lastUpdate)
        .limit(1)
        .to_list()
    )
    if not dbstate:
        return None
    return dbstate[0]


def createDBState(
    action: DBStateActions, collection: DBTables, time_seg: TIME_SEG, docs: Links
) -> DBStateDB:
    match action:
        case "add":
            return DBStateDB(
                table=collection,
                time_seg=time_seg,
                version=get_version(),
                lastUpdate=timestamp_utc_ms(),
                deleted=[],
                added=docs,
                modified=[],
                prev=None,
            )
        case "delete":
            return DBStateDB(
                table=collection,
                time_seg=time_seg,
                version=get_version(),
                lastUpdate=timestamp_utc_ms(),
                deleted=docs,
                added=[],
                modified=[],
                prev=None,
            )
        case "modify":
            return DBStateDB(
                table=collection,
                time_seg=time_seg,
                version=get_version(),
                lastUpdate=timestamp_utc_ms(),
                deleted=[],
                added=[],
                modified=docs,
                prev=None,
            )


async def updateDBState(
    action: DBStateActions, collection: DBTables, time_seg: TIME_SEG, docs: Links
):

    latestDBstate = await get_latest_dbstate("MIN")
    dbState = createDBState(action, collection, time_seg, docs)
    if latestDBstate:
        dbState.prev = latestDBstate

    await dbState.insert()
