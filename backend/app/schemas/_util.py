from pydantic import ConfigDict


def to_camel(snake: str) -> str:
    first, *rest = snake.split("_")
    return first + "".join(word.capitalize() for word in rest)


camel_model_config = ConfigDict(
    alias_generator=to_camel, populate_by_name=True, from_attributes=True
)
