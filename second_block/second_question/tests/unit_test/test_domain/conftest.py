from datetime import date

import pytest

from app.domain.entities.trading_result import TradingResultEntity
from app.domain.values.trading_result import Volume, Total, Count


@pytest.fixture(scope="function")
def entity_trading_result() -> TradingResultEntity:
    sample_data = {
        "exchange_product_id": "1234ABC",
        "exchange_product_name": "Crude Oil",
        "delivery_basis_name": "FOB",
        "volume": Volume(1000),
        "total": Total(50000),
        "count": Count(50),
        "date": date(2023, 1, 1)
    }

    return TradingResultEntity(**sample_data)
