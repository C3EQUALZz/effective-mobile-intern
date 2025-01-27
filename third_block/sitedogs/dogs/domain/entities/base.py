from abc import ABC
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from typing import (
    Any,
    Dict,
    get_type_hints,
    Optional,
    Set,
)
from uuid import uuid4

from dogs.exceptions.domain import CastException


@dataclass(eq=False)
class BaseEntity(ABC):
    """
    Base entity, from which any domain model should be inherited.
    """

    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)

    def __post_init__(self) -> None:
        for field_name, field_type in get_type_hints(self).items():
            if field_name == "oid":
                continue

            value = getattr(self, field_name, None)
            if not isinstance(value, field_type):
                try:
                    setattr(self, field_name, field_type(value))
                except (ValueError, TypeError):
                    raise CastException(f"'{field_name}' with value '{value}' to {field_type}")

    def to_dict(
        self,
        convert_value_object_to_python_object: bool = True,
        exclude: Optional[Set[str]] = None,
        include: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a dictionary representation of the entity.

        convert_value_object_to_python_object: if this field in true, then Value Objects converts to usual
        python objects such as str, int and etc.
        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = asdict(self)

        if convert_value_object_to_python_object:
            data = self.__process_nested(data)

        # Handle exclude set
        if exclude:
            for key in exclude:
                data.pop(key, None)

        # Handle include dictionary
        if include:
            data.update(include)

        return data

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            raise NotImplementedError
        return self.oid == other.oid

    def __hash__(self) -> int:
        return hash(self.oid)

    def __process_nested(self, data: Any) -> Any:
        """Helper function to process nested dictionaries or lists."""
        if isinstance(data, dict):
            # Process dictionaries
            processed = {}
            for key, value in data.items():
                if isinstance(value, dict) and "value" in value:
                    # Replace 'value' with its actual content
                    processed[key] = value["value"]
                else:
                    # Recursively process other dictionaries
                    processed[key] = self.__process_nested(value)
            return processed
        elif isinstance(data, list):
            # Process lists
            return [self.__process_nested(item) for item in data]
        else:
            # Return value as is for other types
            return data
