"""
Run this script from the root of your Django project

Usage:

    pipenv shell
    python manage.py shell

    import load_db_data
    load_db_data.main()
"""


import json
from website.models import Member, Partner, Collaborator, Publication, ResearchField, LabUnit
from lab.models import Material
from django.contrib.auth.models import User


def request_confirm(question, default="no"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
    "request_confirm()" returns True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    choice = input(question + ' [y/N] ').lower()

    if default is not None and choice == '':
        return valid[default]
    elif choice in valid:
        return valid[choice]
    else:
        print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def load_research(filename):
    """Load research fields to ResearchField model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        researchs = json.load(f)

    for research in researchs:
        research = ResearchField(title=research['title'], 
                                content=research['content'])
        research.save()
    
    print(f'{len(researchs)} items added in ResearchField.\n')


def load_lab(filename):
    """Load lab units to LabUnit model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        labs = json.load(f)

    for lab in labs:
        lab = LabUnit(title=lab['title'], 
                    description=lab['description'],
                    equipment=lab['equipment'])
        lab.save()
    
    print(f'{len(labs)} items added in LabUnit.\n')


def load_members(filename):
    """Load current members to Member model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        members = json.load(f)

    for member in members:
        member = Member(name=member['name'], 
                        position=member['position'], 
                        research_area=member['research_area'])
        member.save()
    
    print(f'{len(members)} items added in Member.\n')


def load_alumni(filename):
    """Load alumni to Member model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        members = json.load(f)

    for member in members:
        member = Member(name=member['name'],
                        position=member['position'], 
                        alumni=member['alumni'])
        member.save()
    
    print(f'{len(members)} items added in Member.\n')


def load_collaborations(filename):
    """Load collaborations to Collaborator model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        collabs = json.load(f)

    for collab in collabs:
        collab = Collaborator(name=collab['name'], 
                            affiliation=collab['affiliation'], 
                            scope=collab['scope'],
                            link=collab['link'])
        collab.save()
    
    print(f'{len(collabs)} items added in Collaborator.\n')


def load_partners(filename):
    """Load partners to Partner model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        partners = json.load(f)

    for partner in partners:
        partner = Partner(name=partner['name'], 
                        link=partner['link'])
        partner.save()
    
    print(f'{len(partners)} items added in Partner.\n')


def load_articles(filename):
    """Load articles to Publication model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        articles = json.load(f)

    for article in articles:
        article = Publication(title=article['title'], 
                        authors=article['authors'],
                        issue=article['issue'],
                        journal=article['journal'],
                        volume=article['volume'],
                        year=article['year'],
                        pages=article['pages'],
                        link=article['link'],
                        pub_type=article['pub_type'])
        article.save()
    
    print(f'{len(articles)} items added in Publication.\n')


def load_posters(filename):
    """Load posters to Publication model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        posters = json.load(f)

    for poster in posters:
        poster = Publication(title=poster['title'], 
                        authors=poster['authors'],
                        conference=poster['conference'],
                        conference_city=poster['city'],
                        conference_date=poster['date'],
                        year=poster['year'],
                        pub_type=poster['pub_type'])
        poster.save()
    
    print(f'{len(posters)} items added in Publication.\n')


def load_presentations(filename):
    """Load presentations to Publication model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        presentations = json.load(f)

    for presentation in presentations:
        presentation = Publication(title=presentation['title'], 
                        authors=presentation['authors'],
                        conference=presentation['conference'],
                        conference_city=presentation['city'],
                        conference_date=presentation['date'],
                        year=presentation['year'],
                        pub_type=presentation['pub_type'])
        presentation.save()
    
    print(f'{len(presentations)} items added in Publication.\n')


def load_theses(filename):
    """Load theses to Publication model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        theses = json.load(f)

    for thesis in theses:
        thesis = Publication(title=thesis['title'], 
                            authors=thesis['author'],
                            thesis_type=thesis['thesis_type'],
                            thesis_coordinators=thesis['supervisors'],
                            thesis_institution=thesis['institution'],
                            year=thesis['year'],
                            pub_type='thesis')
        thesis.save()
    
    print(f'{len(theses)} items added in Publication.\n')


def load_inventory_reagents(filename):
    """Load inventory reagents to Material model"""
    with open(f'{filename}.json', encoding="utf-8") as f:
        reagents = json.load(f)

    u = User.objects.get(pk=2)  # Get my user

    for reagent in reagents:
        reagent = Material(name=reagent['name'], 
                        specifications=reagent['comments'],
                        amount=int(reagent['amount']),
                        location=reagent['location'],
                        user=u)
        reagent.save()
    
    print(f'{len(reagents)} items added in Material.\n')


def main():
    if request_confirm('Load research fields?'):
        load_research('initial_data/db_data_research_fields')

    if request_confirm('Load lab units?'):
        load_lab('initial_data/db_data_lab_units')

    if request_confirm('Load members?'):
        load_members('initial_data/db_data_members')

    if request_confirm('Load alumni?'):
        load_alumni('initial_data/db_data_alumni')

    if request_confirm('Load collaborations?'):
        load_collaborations('initial_data/db_data_colab')

    if request_confirm('Load partners?'):
        load_partners('initial_data/db_data_partners')

    if request_confirm('Load articles?'):
        load_articles('initial_data/db_data_articles')
    
    if request_confirm('Load posters?'):
        load_posters('initial_data/db_data_posters')
    
    if request_confirm('Load presentations?'):
        load_presentations('initial_data/db_data_presentations')

    if request_confirm('Load theses?'):
        load_theses('initial_data/db_data_thesis')

    if request_confirm('Load reagents?'):
        load_inventory_reagents('initial_data/db_data_materials')

if __name__ == '__main__':
    main()