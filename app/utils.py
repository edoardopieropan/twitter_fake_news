import json
import csv


def load_json(filepath):
    with open(filepath) as f:
        data = json.load(f)
        return data


def write_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def append_to_csv(filepath, new_row):
    with open(filepath, 'a+', encoding="utf-8") as f:
        w = csv.DictWriter(f, new_row.keys())
        w.writerow(new_row)


def write_csv(filepath, data):
    with open(filepath, 'w', encoding="utf-8") as f:
        w = csv.DictWriter(f, data[0].keys())
        w.writeheader()
        w.writerows(data)


def load_csv(filepath):
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
        return data


