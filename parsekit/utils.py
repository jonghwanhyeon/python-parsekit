def stringify(items):
    for item in items:
        yield str(item) if item is not None else ""
