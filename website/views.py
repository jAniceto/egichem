from django.shortcuts import render
from .models import ResearchField, LabUnit, Partner, Collaborator, Member, Publication


def home(request):
	context = {
		'page_title': 'Home',
	}
	return render(request, 'website/home.html', context)


def research(request):
	context = {
		'page_title': 'Research',
		'page_subtitle': 'Core areas of EGICHEM group',
		'research_fields': ResearchField.objects.all()
	}
	return render(request, 'website/research.html', context)


def lab(request):
	context = {
		'page_title': 'Lab',
		'page_subtitle': 'The EGICHEM laboratory comprises the following research units',
		'lab_units': LabUnit.objects.all()
	}
	return render(request, 'website/lab.html', context)


def partners(request):
	context = {
		'page_title': 'Collaborators',
		'page_subtitle': 'People actively taking part in EGICHEM activities',
		'page_title2': 'Partners',
		'page_subtitle2': 'Companies and entities with which EGICHEM has or had some collaborations',
		'partners': Partner.objects.all().order_by('name'),
		'collaborators': Collaborator.objects.all().order_by('name')
	}
	return render(request, 'website/partners.html', context)
	

def people(request):
	members = Member.objects.all().order_by('name')
	professors = members.filter(highlighted=True)
	postdocs = members.filter(position='PostDoc Researcher').exclude(highlighted=True).exclude(alumni=True)
	phds = members.filter(position='PhD Student').exclude(highlighted=True).exclude(alumni=True)
	fellows = members.filter(position='Research Fellow').exclude(highlighted=True).exclude(alumni=True)
	masters = members.filter(position='MSc Student').exclude(highlighted=True).exclude(alumni=True)
	undergraduates = members.filter(position='Undergraduate Students').exclude(highlighted=True).exclude(alumni=True)

	print(fellows)
	
	context = {
		'page_title': 'People',
		'page_subtitle': 'PostDoc Fellows, PhD Students, Research Fellows, MSc Students and Undergradurate Students',
		'professors': professors,
		'postdocs': postdocs,
		'phds': phds,
		'fellows': fellows,
		'masters': masters,
		'undergraduates': undergraduates,
	}
	return render(request, 'website/people.html', context)


def publications(request):
	publications = Publication.objects.all().order_by('-pk')

	articles = publications.filter(pub_type='article')
	book_chapters = publications.filter(pub_type='book-chapter')
	patents = publications.filter(pub_type='patent')
	posters = publications.filter(pub_type='poster')
	presentations = publications.filter(pub_type='presentation')
	theses = publications.filter(pub_type='thesis')

	context = {
		'page_title': 'Publications',
		'page_subtitle': 'Our publications are divided in the following categories',
		'articles': articles,
		'book_chapters': book_chapters,
		'patents': patents,
		'posters': posters,
		'presentations': presentations,
		'theses': theses,
	}
	return render(request, 'website/publications.html', context)