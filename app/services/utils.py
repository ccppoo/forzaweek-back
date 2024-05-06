from app.schemas.base import MarketCorp, Market

from app.schemas.stat.market import *
from app.schemas.stat.product import *

from app.types import TIME_SEGMENT, MARKET_SEGMENT, PRODUCT_SEGMENT

__all__ = (
    "parse_date",
    "get_market_schema",
    "get_stat_schema",
    "get_prod_stat_schema",
)


def parse_date(date_: str, time_segment: TIME_SEGMENT):
    match (time_segment):
        case "day":
            return {"date": date_}
        case "week":
            yyyy, mm, ww = date_.split("-")
            return {"year_month": f"{yyyy}-{mm}", "week": int(ww)}
        case "month":
            yyyy, mm = date_.split("-")
            return {"year_month": f"{yyyy}-{mm}", "month": int(mm)}
        case "quarter":
            yyyy, qq = date_.split("-")
            return {"year": int(yyyy), "quarter": int(qq)}
        case "year":
            return {"year": int(date_)}


def get_market_schema(market_segment: MARKET_SEGMENT):
    if market_segment == "market":
        return Market

    if market_segment == "market_corp":
        return MarketCorp


def get_stat_schema(market_segment: MARKET_SEGMENT, time_segment: TIME_SEGMENT):

    if market_segment == "none":
        match (time_segment):
            case "day":
                return AllMarketStatDay
            case "week":
                return AllMarketStatWeek
            case "month":
                return AllMarketStatMonth
            case "quarter":
                return AllMarketStatQuarter
            case "year":
                return AllMarketStatYear

    if market_segment == "market":
        match (time_segment):
            case "day":
                return MarketStatDay
            case "week":
                return MarketStatWeek
            case "month":
                return MarketStatMonth
            case "quarter":
                return MarketStatQuarter
            case "year":
                return MarketStatYear

    if market_segment == "market_corp":
        match (time_segment):
            case "day":
                return MarketCorpStatDay
            case "week":
                return MarketCorpStatWeek
            case "month":
                return MarketCorpStatMonth
            case "quarter":
                return MarketCorpStatQuarter
            case "year":
                return MarketCorpStatYear


def get_prod_stat_schema(
    market_segment: MARKET_SEGMENT,
    prod_segment: PRODUCT_SEGMENT,
    time_segment: TIME_SEGMENT,
):
    # prod_segment != none

    if market_segment == "none":
        if prod_segment == "product_family":
            match (time_segment):
                case "day":
                    return AllMarketProductFamilyStatDay
                case "week":
                    return AllMarketProductFamilyStatWeek
                case "month":
                    return AllMarketProductFamilyStatMonth
                case "quarter":
                    return AllMarketProductFamilyStatQuarter
                case "year":
                    return AllMarketProductFamilyStatYear
        if prod_segment == "product_detailed":
            match (time_segment):
                case "day":
                    return AllMarketProductStatDay
                case "week":
                    return AllMarketProductStatWeek
                case "month":
                    return AllMarketProductStatMonth
                case "quarter":
                    return AllMarketProductStatQuarter
                case "year":
                    return AllMarketProductStatYear

    if market_segment == "market":
        if prod_segment == "product_family":
            match (time_segment):
                case "day":
                    return MarketProductFamilyStatDay
                case "week":
                    return MarketProductFamilyStatWeek
                case "month":
                    return MarketProductFamilyStatMonth
                case "quarter":
                    return MarketProductFamilyStatQuarter
                case "year":
                    return MarketProductFamilyStatYear
        if prod_segment == "product_detailed":
            match (time_segment):
                case "day":
                    return MarketProductStatDay
                case "week":
                    return MarketProductStatWeek
                case "month":
                    return MarketProductStatMonth
                case "quarter":
                    return MarketProductStatQuarter
                case "year":
                    return MarketProductStatYear

    if market_segment == "market_corp":
        if prod_segment == "product_family":
            match (time_segment):
                case "day":
                    return MarketCorpProductFamilyStatDay
                case "week":
                    return MarketCorpProductFamilyStatWeek
                case "month":
                    return MarketCorpProductFamilyStatMonth
                case "quarter":
                    return MarketCorpProductFamilyStatQuarter
                case "year":
                    return MarketCorpProductFamilyStatYear
        if prod_segment == "product_detailed":
            match (time_segment):
                case "day":
                    return MarketCorpProductStatDay
                case "week":
                    return MarketCorpProductStatWeek
                case "month":
                    return MarketCorpProductStatMonth
                case "quarter":
                    return MarketCorpProductStatQuarter
                case "year":
                    return MarketCorpProductStatYear
