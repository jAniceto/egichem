import datetime
from django.shortcuts import render
from django.http import Http404
from django.db.models import Q
from .models import MainResearchArea, ResearchField, LabUnit, Partner, Collaborator, Member, Publication, Tool, Award
from blog.models import Post

import re


def format_scientific_name(name):
    """Creates several name formats."""
    names_and_initials = re.split('\W+', name)
    name_number = len(names_and_initials)
    name_fmt_1 = ''  # F.X.Y. Lastname
    name_fmt_2 = ''  # F. Lastname
    name_fmt_3 = ''  # F. X. Y. Lastname
    name_fmt_4 = ''  # First X. Y. Lastname
    for i, n in enumerate(names_and_initials):
        if i == name_number-1:
            name_fmt_1 += ' ' + n
            name_fmt_2 += ' ' + n
            name_fmt_3 += n
            name_fmt_4 += n
        else:
            name_fmt_1 += n[0] + '.'
            if i == 0:
                name_fmt_2 += n[0] + '.'
                name_fmt_4 += n + ' '
            else:
                name_fmt_4 += n[0] + '. '
            name_fmt_3 += n[0] + '. '
    # return [name_fmt_1, name_fmt_2, name_fmt_3, name_fmt_4]
    return [name_fmt_1, 'F. Lastname', name_fmt_3, name_fmt_4]


def home(request):
    main_research_areas = MainResearchArea.objects.all().order_by('order', 'title')
    publications = Publication.objects.all()
    members = Member.objects.all()
    awards = Award.objects.all()
    latest_posts = Post.objects.all().order_by('-date_posted')[:3]
    latest_publications = publications.order_by('-year', '-date_added')[:5]

    context = {
        'page_title': 'Home',
        'latest_posts': latest_posts,
        'latest_publications': latest_publications,
        'main_research_areas': main_research_areas,
        # Metrics
        'articles': publications.filter(pub_type='article').count(),
        'book_chapters': publications.filter(pub_type='book-chapter').count(),
        'patents': publications.filter(pub_type='patent').count(),
        'awards': awards.count(),
        'communications': publications.filter(pub_type='presentation').count() + publications.filter(pub_type='poster').count(),
        # 'projects': '9',
        'MSc_completed': publications.filter(pub_type='thesis', thesis_type='MSc').count(),
        'MSc_oncourse': members.filter(position='PhD Student').exclude(alumni=True).count(),
        'fellows_completed': members.filter(position='Research Fellow').exclude(alumni=False).count(),
        'fellows_oncourse': members.filter(position='Research Fellow').exclude(alumni=True).count(),
        'PhD_completed': publications.filter(pub_type='thesis', thesis_type='PhD').count(),
        'PhD_oncourse': members.filter(position='PhD Student').exclude(alumni=True).count(),
        'postdocs_completed': members.filter(position='PostDoc Researcher').exclude(alumni=False).count() + members.filter(position='Researcher').count(),
        'postdocs_oncourse': members.filter(position='PostDoc Researcher').exclude(alumni=True).count(),
        'visiting': members.filter(visiting=True).count(),
    }
    return render(request, 'website/home.html', context)


def research(request):
    context = {
        'page_title': 'Research',
        'page_subtitle': 'Main research areas of EgiChem',
        'research_fields': ResearchField.objects.all().order_by('order', '-date_added')
    }
    return render(request, 'website/research.html', context)


def lab(request):
    context = {
        'page_title': 'Lab',
        'page_subtitle': 'Research units and equipment',
        'lab_units': LabUnit.objects.all().order_by('order','-date_added')
    }
    return render(request, 'website/lab.html', context)


def partners(request):
    context = {
        'page_title': 'Collaborators',
        'page_subtitle': 'Academic collaborations',
        'page_title2': 'Partners',
        'page_subtitle2': 'Companies that have worked with EgiChem',
        'partners': Partner.objects.all().order_by('name'),
        'collaborators': Collaborator.objects.all().order_by('name')
    }
    return render(request, 'website/partners.html', context)


def people(request):
    members = Member.objects.all().order_by('name')
    professors = members.filter(highlighted=True)
    researchers = members.filter(position='Researcher').exclude(highlighted=True).exclude(alumni=True)
    postdocs = members.filter(position='PostDoc Researcher').exclude(highlighted=True).exclude(alumni=True)
    phds = members.filter(position='PhD Student').exclude(highlighted=True).exclude(alumni=True)
    fellows = members.filter(position='Research Fellow').exclude(highlighted=True).exclude(alumni=True)
    masters = members.filter(position='MSc Student').exclude(highlighted=True).exclude(alumni=True)
    undergraduates = members.filter(position='Undergraduate Student').exclude(highlighted=True).exclude(alumni=True)
    alumni_researchers = members.filter(alumni=True, position='Researcher')
    alumni_postdocs = members.filter(alumni=True, position='PostDoc Researcher')
    alumni_phds = members.filter(alumni=True, position='PhD Student')
    alumni_fellows = members.filter(alumni=True, position='Research Fellow')
    alumni_masters = members.filter(alumni=True, position='MSc Student')
    alumni_undergraduates = members.filter(alumni=True, position='Undergraduate Student')

    context = {
        'page_title': 'People',
        'page_subtitle': 'EgiChem Team',
        'professors': professors,
        'researchers': researchers,
        'postdocs': postdocs,
        'phds': phds,
        'fellows': fellows,
        'masters': masters,
        'undergraduates': undergraduates,
        'alumni_researchers': alumni_researchers,
        'alumni_postdocs': alumni_postdocs,
        'alumni_phds': alumni_phds,
        'alumni_fellows': alumni_fellows,
        'alumni_masters': alumni_masters,
        'alumni_undergraduates': alumni_undergraduates,
    }
    return render(request, 'website/people.html', context)


def publications(request):
    publications = Publication.objects.all().order_by('-year', '-date_added')
    articles = publications.filter(pub_type='article')
    book_chapters = publications.filter(pub_type='book-chapter')
    patents = publications.filter(pub_type='patent')
    posters = publications.filter(pub_type='poster')
    presentations = publications.filter(pub_type='presentation')
    theses = publications.filter(pub_type='thesis')
    phd_theses = theses.filter(thesis_type='PhD')
    msc_theses = theses.filter(thesis_type='MSc')

    context = {
        'page_title': 'Publications',
        'page_subtitle': '',
        'articles': articles,
        'book_chapters': book_chapters,
        'patents': patents,
        'posters': posters,
        'presentations': presentations,
        'theses': theses,
        'phd_theses': phd_theses,
        'msc_theses': msc_theses,
        'current_year': datetime.datetime.today().year,
    }
    return render(request, 'website/publications.html', context)


def member_page(request, name_slug):
    try:
        member = Member.objects.get(slug=name_slug)
        if member.user and member.user.profile and member.user.profile.scientific_name:
            # If member has a user profile get the scientific name from there
            scientific_name = format_scientific_name(member.user.profile.scientific_name)
        else:
            # If member does not have a user profile create a scientific name based on the member name
            scientific_name = format_scientific_name(member.name)

        # Get member publications based on two possible scientific names
        member_pubs = Publication.objects.filter(
            Q(authors__contains=scientific_name[0]) | 
            Q(authors__contains=scientific_name[1]) |
            Q(authors__contains=scientific_name[2]) |
            Q(authors__contains=scientific_name[3])
        )
        member_articles = member_pubs.filter(pub_type='article').order_by('-year', 'title')
        member_book_chapters = member_pubs.filter(pub_type='book-chapter').order_by('-year', 'title')
        member_patents = member_pubs.filter(pub_type='patent').order_by('-year', 'title')
        member_posters = member_pubs.filter(pub_type='poster').order_by('-year', 'title')
        member_presentations = member_pubs.filter(pub_type='presentation').order_by('-year', 'title')
        member_theses = member_pubs.filter(pub_type='thesis').order_by('-year', 'title')

        context = {
            'page_title': member.name,
            'member': member,
            'member_articles': member_articles,
            'member_book_chapters': member_book_chapters,
            'member_patents': member_patents,
            'member_posters': member_posters,
            'member_presentations': member_presentations,
            'member_theses': member_theses,
        }

    except Member.DoesNotExist:
        raise Http404("Member page does not exist.")

    return render(request, 'website/member.html', context)


def tools(request):
    tools = Tool.objects.all().order_by('-date_added')

    context = {
        'page_title': 'Tools',
        'page_subtitle': 'Programs developed by the EgiChem group',
        'tools': tools,
    }    
    return render(request, 'website/tools.html', context)


def awards(request):
    awards = Award.objects.all().order_by('-date_added')

    context = {
        'page_title': 'Awards',
        'page_subtitle': '',
        'awards': awards,
    }
    return render(request, 'website/awards.html', context)