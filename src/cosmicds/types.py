from pydantic import field_serializer
from typing import Any, Type, Callable, TypeVar
from pydantic_core import core_schema
from copy import deepcopy

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    ValidationError,
)
from pydantic.json_schema import JsonSchemaValue
from solara import Reactive
from typing_extensions import Annotated


# TODO: Revisit this in the future. We are monkey patching the `Reactive` class
#  to support deepcopy for serialization. This is something to talk to Maarten
#  about having in Solara proper.
def __override_deepcopy__(self, memo):
    return self.__class__(deepcopy(self.value, memo))


Reactive.__deepcopy__ = __override_deepcopy__


class _ReactiveTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_any(value: Any) -> Reactive:
            return Reactive(value)

        from_any_schema = core_schema.chain_schema(
            [
                core_schema.any_schema(),
                core_schema.no_info_plain_validator_function(validate_from_any),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_any_schema,
            python_schema=core_schema.union_schema(
                [
                    # Check if it's an instance first before doing any
                    #  further work
                    core_schema.is_instance_schema(Reactive),
                    from_any_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.value,
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.any_schema())


T = TypeVar("T")
PydanticReactive = Annotated[
    Reactive[T], _ReactiveTypePydanticAnnotation
]
