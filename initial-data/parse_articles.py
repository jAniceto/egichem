import re
import json
import datetime


def parse_ref(refs):
    split_text = refs.split('.', 1)
    id = split_text[0]
    ref = split_text[1]

    sections = ref.split(',')

    raw_authors = sections[:-3]
    authors = [x.strip(' ') for x in raw_authors]

    title = sections[-2].strip(' ')

    journal_info = sections[-1]
    try:
        journal = re.search(r'[^\d]*', journal_info).group().strip(' ')
    except AttributeError:
        journal = None
    
    # Get journal volume and issue
    try:    
        journal_vol_issue = re.search(r'\d+:\d+', journal_info).group()
    except AttributeError:
        try:    
            journal_vol_issue = re.search(r'\d+ \(', journal_info).group().strip(' (')
        except AttributeError:
            journal_vol_issue = None

    # Get year
    try:
        year = re.search(r'\(\d+\)', journal_info).group().strip('(').strip(')')
    except AttributeError:
        year = None

    # Get pages
    try:
        pages = re.search(r'\d+-\d+', journal_info).group()
    except AttributeError:
        pages = None


    ref_dict = {
        'id': id,
        'authors': authors,
        'first_author': authors[0],
        'title': title,
        'journal': journal,
        'vol_issue': journal_vol_issue,
        'year': year,
        'pages': pages,
        }

    return ref_dict


def load_pub_text(filename):
    with open(filename) as f:
        raw_lines = f.readlines()

    lines = [x for x in raw_lines if (x != '\n') and (x != 'View\n') and (len(x) > 10)]
    ref_list = [x.strip('\n') for x in lines]
    return ref_list


def build_fixture(filename, ref_list, model, pub_type):
    fixture = []
    for ref in ref_list:
        fixture.append({
            'pk': ref['id'],
            'model': model,
            'fields': {
                'type': pub_type,
                'authors': json.dumps(ref['authors'], ensure_ascii=False),
                'first_author': ref['first_author'],
                'title': ref['title'],
                'journal': ref['journal'],
                'vol_issue': ref['vol_issue'],
                'year': ref['year'],
                'pages': ref['pages'],
                'url': None,
                'date_added': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        })

    with open(filename, 'w') as fp:
        json.dump(fixture, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    item_list = load_pub_text('references.txt')
    
    all_refs = []
    for item in item_list:
        all_refs.append(parse_ref(item))
    
    build_fixture('publications_fixture.json', all_refs, 'website.Publication', 'Article')

    