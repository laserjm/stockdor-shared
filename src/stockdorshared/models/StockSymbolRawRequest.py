from typing import Any, List, Optional
from pydantic import BaseModel


class StockSymbolRawRequest(BaseModel):
    symbol: Optional[str]
    Profile: Optional[Any]
    IncomeStatementsAnnual: Optional[List[Any]]
    IncomeStatementsQuarterly: Optional[List[Any]]
    CashflowStatementsAnnual: Optional[List[Any]]
    FinancialRatiosAnnual: Optional[List[Any]]
    HistoricalDividends: Optional[List[Any]]
