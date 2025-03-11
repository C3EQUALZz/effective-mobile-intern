import pytest
from app.domain.values.trading_result import Volume
from app.exceptions.domain import VolumeException
from contextlib import nullcontext as does_not_raise
from typing import ContextManager


class TestVolume:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (0, does_not_raise()),
            (1, does_not_raise()),
            (500, does_not_raise()),
            (9999, does_not_raise()),
            (-1, pytest.raises(VolumeException)),
            (-100, pytest.raises(VolumeException)),
            (-9999, pytest.raises(VolumeException)),
        ]
    )
    def test_volume_value_attr_and_method(self, value: int, expected: ContextManager) -> None:
        with expected:
            volume = Volume(value)
            assert volume.value == value == volume.as_generic_type()
            assert isinstance(volume.as_generic_type(), int)

    @pytest.mark.parametrize("value", [1, 100, 9999])
    def test_volume_as_generic_type_returns_int(self, value: int) -> None:
        volume = Volume(value)
        generic_value = volume.as_generic_type()

        assert isinstance(generic_value, int)
        assert generic_value == value

    def test_volume_validate_direct_call(self) -> None:
        valid_volume = Volume(100)
        assert valid_volume.validate() is None

        # Чтобы протестировать validate напрямую, обходим frozen dataclass через __new__
        invalid_volume = Volume.__new__(Volume)
        object.__setattr__(invalid_volume, 'value', -1)

        with pytest.raises(VolumeException):
            invalid_volume.validate()
