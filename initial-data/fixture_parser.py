import json


def load_fixture(filename):
    with open(f'{filename}.json', encoding="utf-8") as f:
        fixture = json.load(f)
    return fixture


def save_db_data(data, filename):
    with open(f'{filename}.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, indent=4)


def parse_research_fields():
    fixt = load_fixture('db_dump')

    MODEL_NAME = 'website.researchfield'
    db_item = []
    for item in fixt:
        if item['model'] == MODEL_NAME:
            db_item.append({
                'title': item['fields']['title'],
                'content': item['fields']['content']
            })

    save_db_data(db_item, 'db_data_research_fields')


def parse_lab_unis():
    fixt = load_fixture('db_dump')

    MODEL_NAME = 'website.labunit'
    db_item = []
    for item in fixt:
        if item['model'] == MODEL_NAME:
            db_item.append({
                'title': item['fields']['title'],
                'description': item['fields']['description'],
                'equipment': item['fields']['equipment']
            })

    save_db_data(db_item, 'db_data_lab_units')


def parse_articles():
    fixt = load_fixture('articles')

    MODEL_NAME = 'website.publication'
    db_item = []
    for item in fixt:
        if item['model'] == MODEL_NAME:
            db_item.append({
            "pub_type": item['fields']['pub_type'],
            "authors": item['fields']['authors'],
            "title": item['fields']['title'],
            "year": item['fields']['year'],
            "journal": item['fields']['journal'],
            "volume": item['fields']['volume'],
            "issue": item['fields']['issue'],
            "pages": item['fields']['pages'],
            "link": item['fields']['link']
        })

    save_db_data(db_item, 'db_data_articles')


if __name__ == "__main__":
    parse_articles()