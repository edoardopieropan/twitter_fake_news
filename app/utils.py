import json


def load_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
        return data


def write_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
