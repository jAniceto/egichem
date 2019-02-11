import csv
import re
import json


def parse_csv_to_json(filename):
    # Load CSV file to check number of lines
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader_temp = csv.reader(csv_file, delimiter=',')
        pub_total = sum(1 for x in csv_reader_temp)

    # Load CSV file again
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        article_list = []
        fixture = []
        pub_count = 0

        for row in csv_reader:
            if pub_count == 0:
                pub_count += 1
            else:
                # authors = re.findall(r'[\w-]+, [\w.]+', row[0])  # re fails on special characters like ã
                authors = re.findall(r'[A-Za-zÀ-ÿ]+, [\w.-]+', row[0])

                authors_reordered = []
                for author in authors:
                    names = author.split(', ')
                    authors_reordered.append(f'{names[1]} {names[0]}')

                authors_str = ', '.join(authors_reordered)

                # Build simple dict
                article_list.append({
                    'authors': authors_str,
                    'first_author': authors_reordered[0],
                    'title': row[2],
                    'year': row[3],
                    'journal': row[4],
                    'volume': row[5],
                    'issue': row[6],
                    'pages': f'{row[8]}-{row[9]}',
                    'doi': row[12],
                    'link': row[13],
                    'status': row[15]
                })

                # Build fixture for Django DB
                fixture.append({
                    'pk': pub_total - pub_count,
                    'model': 'website.publication',
                    'fields': {
                        'pub_type': 'article',
                        'authors': authors_str,
                        # 'first_author': authors[0],
                        'title': row[2],
                        'year': row[3],
                        'journal': row[4],
                        'volume': row[5],
                        'issue': row[6],
                        'pages': f'{row[8]}-{row[9]}',
                        # 'doi': row[12],
                        'link': row[13],
                    }
                })

                pub_count += 1

    # Save JSON json
    with open('articles.json', 'w', encoding="utf-8") as fp:
        json.dump(fixture, fp, indent=4, ensure_ascii=False)

    return article_list


if __name__ == "__main__":
    parse_csv_to_json('scopus_export.csv')
