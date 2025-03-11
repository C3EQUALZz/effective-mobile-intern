import pytest
from app.domain.values.trading_result import Count
from app.exceptions.domain import CountException
from contextlib import nullcontext as does_not_raise
from typing import ContextManager


class TestCount:
    @pytest.mark.parametrize("valid_value", [0, 1, 100, 9999])
    def test_count_valid_values(self, valid_value: int) -> None:
        count = Count(valid_value)
        assert count.value == valid_value
        assert count.as_generic_type() == valid_value


    @pytest.mark.parametrize(
        "value, expected",
        [
            (-1, pytest.raises(CountException)),
            (-10, pytest.raises(CountException)),
            (-999, pytest.raises(CountException)),
            (10, does_not_raise())
        ]
    )
    def test_count_invalid_values_raise_exception(self, value: int, expected: ContextManager) -> None:
        with expected:
            Count(value)

    
    def test_count_as_generic_type(self) -> None:
        count = Count(42)
        assert isinstance(count.as_generic_type(), int)
        assert count.as_generic_type() == 42
