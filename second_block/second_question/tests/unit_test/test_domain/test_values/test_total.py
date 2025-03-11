import pytest
from app.domain.values.trading_result import Total
from app.exceptions.domain import TotalException
from contextlib import nullcontext as does_not_raise


class TestTotal:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (1000, does_not_raise()),
            (999999, does_not_raise()),
            (-1, pytest.raises(TotalException)),
            (-10, pytest.raises(TotalException)),
            (-99999, pytest.raises(TotalException))
        ]
    )
    def test_total_valid_values(self, value, expected) -> None:
        with expected:
            total = Total(value)

            assert total.value == value
            assert total.as_generic_type() == value

    # Проверка метода as_generic_type()
    def test_total_as_generic_type_returns_int(self) -> None:
        total = Total(500)
        generic_value = total.as_generic_type()

        assert isinstance(generic_value, int)
        assert generic_value == 500

    # Прямой вызов validate(), если нужен низкоуровневый тест
    def test_total_validate_direct_call(self) -> None:
        total = Total(123)
        assert total.validate() is None

        # Обход ограничения frozen dataclass через __new__ + object.__setattr__
        invalid_total = Total.__new__(Total)
        object.__setattr__(invalid_total, 'value', -100)

        with pytest.raises(TotalException):
            invalid_total.validate()
