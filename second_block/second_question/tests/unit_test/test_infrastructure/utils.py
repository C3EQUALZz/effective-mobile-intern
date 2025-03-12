from dataclasses import dataclass, asdict
from datetime import date
from typing import Dict, Any

from app.domain.values.trading_result import Volume, Total, Count


@dataclass
class BaseTestConfig:

    def to_dict(self, to_lower: bool = False) -> Dict[str, Any]:
        base_dict: Dict[str, Any] = asdict(self)
        if to_lower:
            return {k.lower(): v for k, v in base_dict.items()}

        return base_dict


@dataclass
class FakeTradingResultConfig(BaseTestConfig):
    OID: str = "0866a2c2-a9fe-4f45-885b-11c4e3d2b102"
    EXCHANGE_PRODUCT_ID: str = 'A100ANK060F'
    EXCHANGE_PRODUCT_NAME: str = "Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)"
    DELIVERY_BASIS_NAME: str = "Ангарск-группа станций"
    VOLUME: int = Volume(60)
    TOTAL: int = Total(4000000)
    COUNT: int = Count(1)
    DATE: date = date.today()
