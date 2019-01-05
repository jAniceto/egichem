from django.shortcuts import render
from .models import ResearchField, LabUnit, Partner, Collaborator, Member


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


def publications(request, pub_type):

	context = {
		'page_title': pub_type,
		'page_subtitle': 'Our publications are divided in the following categories',
		'pub_type': pub_type
	}
	return render(request, 'website/publications.html', context)