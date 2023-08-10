from typing import Optional
from pydantic import BaseModel


class StockSymbolRichRequest(BaseModel):
    symbol: Optional[str]
    logo: Optional[str]
    company_name: Optional[str]
    isin: Optional[str]
    symbol: Optional[str]
    price: Optional[float]
    country: Optional[str]
    currency: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    market_cap: Optional[float]
    # dividend block start!!!!
    dividend_num_annual_payments: Optional[int]
    dividend_total_annual: Optional[float]
    dividend_total_ttm: Optional[float]
    dividend_yield_annual: Optional[float]
    dividend_yield_annual_price_before_payout: Optional[float]
    dividend_yield_ttm: Optional[float]
    dividend_payout_ratio_annual_net_income: Optional[float]
    dividend_payout_ratio_annual_free_cash_flow: Optional[float]
    dividend_consecutive_yearsraises: Optional[float]
    dividend_years_no_lowered: Optional[float]
    dividend_growth_5yr_arithmetic: Optional[float]
    dividend_growth_10yr_arithmetic: Optional[float]
    dividend_growth_5yr_cagr: Optional[float]
    dividend_growth_10yr_cagr: Optional[float]
