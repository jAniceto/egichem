import csv
import json
import pprint


# Load CSV file to check number of lines´
def load_csv(filename):
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
    
        item_list = []
        for row in csv_reader:
            item_list.append(row)

    return item_list



def build_db_data_presentations(ref_list, pub_type):
    db_data = []
    for ref in ref_list:
        db_data.append({
            'title': ref[1],
            'authors': ref[0],
            'conference': ref[2],
            'city': ref[3],
            'country': ref[4],
            'date': ref[5],
            'year': ref[6],
            'pub_type': pub_type,
        })
    
    return db_data


def create_json(filename, db_data):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(db_data, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    presentation_list = load_csv('posters.csv')
    presentations = build_db_data_presentations(presentation_list, 'Poster')

    create_json('db_data_posters.json', presentations)