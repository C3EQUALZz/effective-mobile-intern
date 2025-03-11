from datetime import datetime, date, UTC

import pytest

from app.domain.entities.trading_result import TradingResultEntity
from app.domain.values.trading_result import Volume, Total, Count


class TestTradingResultEntity:
    def test_entity_initialization(self, entity_trading_result: TradingResultEntity) -> None:
        assert entity_trading_result.exchange_product_id == "1234ABC"
        assert entity_trading_result.exchange_product_name == "Crude Oil"
        assert entity_trading_result.delivery_basis_name == "FOB"

        assert isinstance(entity_trading_result.volume, Volume)
        assert isinstance(entity_trading_result.total, Total)
        assert isinstance(entity_trading_result.count, Count)

        assert entity_trading_result.volume.value == 1000
        assert entity_trading_result.total.value == 50000
        assert entity_trading_result.count.value == 50

        assert entity_trading_result.date == date(2023, 1, 1)

    def test_computed_properties(self, entity_trading_result: TradingResultEntity) -> None:
        assert entity_trading_result.oil_id == "1234"
        assert entity_trading_result.delivery_basis_id == "ABC"
        assert entity_trading_result.delivery_type_id == "C"


    def test_created_on_default(self, entity_trading_result) -> None:
        today = datetime.now(UTC).date()

        assert entity_trading_result.created_on == today
        assert entity_trading_result.updated_on == today

    @pytest.mark.parametrize(
        "exchange_product_id, exchange_product_name, delivery_basis_name, volume_value, total_value, count_value, result_date, custom_date",
        [
            (
                    "9012DEF",
                    "Jet Fuel",
                    "DAP",
                    500,
                    25000,
                    30,
                    date(2024, 2, 20),
                    date(2022, 12, 31)
            ),
            (
                    "1234ABC",
                    "Crude Oil",
                    "FOB",
                    1000,
                    50000,
                    50,
                    date(2023, 1, 1),
                    date(2023, 5, 15)
            ),
            (
                    "5678XYZ",
                    "Diesel Fuel",
                    "CIF",
                    2000,
                    100000,
                    80,
                    date(2023, 6, 1),
                    date(2023, 7, 10)
            ),
        ]
    )
    def test_custom_created_on_updated_on(
            self,
            exchange_product_id,
            exchange_product_name,
            delivery_basis_name,
            volume_value,
            total_value,
            count_value,
            result_date,
            custom_date
    ) -> None:
        entity = TradingResultEntity(
            exchange_product_id=exchange_product_id,
            exchange_product_name=exchange_product_name,
            delivery_basis_name=delivery_basis_name,
            volume=Volume(volume_value),
            total=Total(total_value),
            count=Count(count_value),
            date=result_date,
            created_on=custom_date,
            updated_on=custom_date
        )

        assert entity.created_on == custom_date
        assert entity.updated_on == custom_date
        assert entity.exchange_product_id == exchange_product_id
        assert entity.exchange_product_name == exchange_product_name
        assert entity.delivery_basis_name == delivery_basis_name
        assert entity.volume.value == volume_value
        assert entity.total.value == total_value
        assert entity.count.value == count_value
        assert entity.date == result_date
