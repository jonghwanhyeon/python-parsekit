from typing import Any, Iterable


def stringify(items):
    for item in items:
        yield str(item) if item is not None else ""


def flatten(iterable: Iterable[Any]) -> Any:
    for item in iterable:
        if item is None:
            continue

        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
