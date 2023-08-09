from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from stockdorshared.models.PyObjectId import PyObjectId


class StockSymbolRichRequest(BaseModel):
    symbol: Optional[str]
    dividend_yield: Optional[float]  # Dividendenrendite
    dividend_yield_calculated: Optional[float]  # self calculated
    dividend_growth_avg_last_5y: Optional[float]  # Dividendenwachstum -- own calc
    dividend_cagr_5y: Optional[float]  # Compound Annual Growth Rate
    dividend_payout_ratio: Optional[float]  # Ausschüttungsquote --
    dividend_payout_ratio_calc: Optional[float]  # Ausschüttungsquote -- own calc
    dividend_payout_ratio_cash: Optional[float]  # Ausschüttungsquote Cash --
