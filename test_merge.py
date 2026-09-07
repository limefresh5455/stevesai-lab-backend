def deep_merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(destination.get(key), dict):
            deep_merge(value, destination[key])
        else:
            destination[key] = value
    return destination

db_data = {
    "title": "Old Title",
    "content": {
        "hero": "old hero",
        "faqs": ["old faq"]
    }
}

incoming = {
    "title": "New Title",
    "content": {
        "hero": "new hero"
    }
}

merged = deep_merge(incoming, db_data)
print(merged)
