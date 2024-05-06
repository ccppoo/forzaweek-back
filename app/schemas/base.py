from pydantic import (
    BaseModel,
    Field,
)
from typing import Optional

__all__ = (
    "_AuctionStat",
    "_MarketStat",
    "_MarketCorpStat",
    "_AllMarketStat",
    "_AllMarketProductFamilyStat",
    "_MarketProductFamilyStat",
    "_MarketCorpProductFamilyStat",
    "_AllMarketProductStat",
    "_MarketProductStat",
    "_MarketCorpProductStat",
)


class _AuctionStat(BaseModel):
    kg_total: float = Field(description="경매 총 물량 (단위: kg)")
    sell_total: int = Field(description="경매 총 액 (단위: 원)")
    auction_total: int = Field(description="하루에 진행한 경매 총 횟수")


class _ProductStat(BaseModel):
    """
    평균 가격, 하위 20% 경계, 상위 80% 경계 값 기준으로 가격 상하단
    """

    avg_kg_price: int = Field(description="낙찰 가격 평균")
    total_avg_kg_price: int = Field(description="전체 물량/전체 낙찰 가격")
    percentage_20: int = Field(description="전체 가격 20%")
    percentage_80: int = Field(description="전체 가격 80%")


class ProductFamily(BaseModel):
    id: str = Field(description="제품군 ID", min_length=4, max_length=4)
    name: str = Field(description="제품군 이름")


class ProductDetailed(BaseModel):
    id: str = Field(description="제품 ID", min_length=6, max_length=6)
    name: str = Field(description="제품 이름")


class Market(BaseModel):
    id: str = Field(description="경매 시장 ID")
    name: str = Field(description="경매 시장 이름")


class MarketCorp(BaseModel):
    id: str = Field(description="경매 법인 ID")
    name: str = Field(description="경매 법인 이름")

    @property
    def is_joint_market(self) -> bool:
        if self.name.endswith("(공)"):
            return True
        return False


class _ProductFamilyStatBase(_ProductStat):
    """
    제품군(id 4자리) 스탯
    """

    product: ProductFamily


class _ProductDetailedStatBase(_ProductStat):
    """
    제품(id 6자리) 스탯
    """

    product: ProductDetailed


class _AllMarketProductFamilyStat(_ProductFamilyStatBase):
    """
    모든 경매시장 제품군 스탯
    """

    pass


class _MarketProductFamilyStat(_ProductFamilyStatBase):
    """
    경매시장 제품군 스탯
    """

    market: Market = Field(description="경매 시장")


class _MarketCorpProductFamilyStat(_ProductFamilyStatBase):
    """
    경매시장 법인 제품군 스탯
    """

    market_corp: MarketCorp = Field(description="경매시장 법인")


class _AllMarketProductStat(_ProductDetailedStatBase):
    """
    모든 경매시장 제품 스탯
    """

    pass


class _MarketProductStat(_ProductDetailedStatBase):
    """
    경매시장 제품 스탯
    """

    market: Market = Field(description="경매 시장")


class _MarketCorpProductStat(_ProductDetailedStatBase):
    """
    경매시장 법인 제품 스탯
    """

    market_corp: MarketCorp = Field(description="경매시장 법인")


## market


class _MarketStatBase(_AuctionStat):
    products_treated: int = Field(description="경매 진행한 품목 수", default=None)


class _AllMarketStat(_MarketStatBase):
    """
    모든 경매시장 schema
    """


class _MarketStat(_MarketStatBase):
    """
    경매시장 schema
    """

    market: Market = Field(description="경매 시장")


class _MarketCorpStat(_MarketStatBase):
    """
    경매시장 법인 schema
    """

    market_corp: MarketCorp = Field(description="경매시장 법인")


## product

# class _ProductStat
