import csv
import json
import pprint


# Load CSV file to check number of lines´
def load_csv(filename):
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
    
        item_list = []
        count = 0
        for row in csv_reader:
            item_list.append(row)

    return item_list



def build_db_data_phds(ref_list, pub_type):
    db_data = []
    for ref in ref_list:
        db_data.append({
            'title': ref[1],
            'author': ref[0],
            'supervisors': ref[2],
            'institution': ref[3],
            'year': ref[4],
            'thesis_type': pub_type,
        })
    
    return db_data


def build_db_data_masters(ref_list, pub_type):
    db_data = []
    for ref in ref_list:
        db_data.append({
            'title': ref[1],
            'author': ref[0],
            'master_thesis_type': ref[2],
            'supervisors': ref[3],
            'institution': ref[4],
            'year': ref[5],
            'thesis_type': pub_type,
        })
    
    return db_data


def create_json(filename, db_data):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(db_data, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    phd_list = load_csv('phds.csv')
    phds = build_db_data_phds(phd_list, 'PhD')

    masters_list = load_csv('masters.csv')
    masters = build_db_data_masters(masters_list, 'MSc')

    create_json('db_data_thesis.json', phds + masters)