from parse_presentations import load_csv, create_json


def build_db_data_materials(ref_list):
    db_data = []
    for ref in ref_list:
        db_data.append({
            'name': ref[0],
            'amount': ref[1],
            'location': ref[3],
            'comments': ref[2],
        })
    
    return db_data


if __name__ == '__main__':
    materials_list = load_csv('materials.csv')
    materials = build_db_data_materials(materials_list)

    create_json('db_data_materials.json', materials)