import datetime
from django.shortcuts import render
from django.http import Http404
from .models import ResearchField, LabUnit, Partner, Collaborator, Member, Publication, Tool, Award
from blog.models import Post


def home(request):
	latest_posts = Post.objects.all().order_by('-date_posted')[:5]
	
	publications = Publication.objects.all()
	members = Member.objects.all()
	awards = Award.objects.all()
	
	context = {
		'page_title': 'Home',
		'latest_posts': latest_posts,
		'articles': publications.filter(pub_type='article').count(),
		'book_chapters': publications.filter(pub_type='book-chapter').count(),
		'patents': publications.filter(pub_type='patent').count(),
		'awards': awards.count(),
		'communications': publications.filter(pub_type='presentation').count(),
		# 'projects': '9',
		'MSc_completed': publications.filter(pub_type='thesis', thesis_type='MSc').count(),
		'MSc_oncourse': members.filter(position='PhD Student').exclude(alumni=True).count(),
		'fellows_completed': members.filter(position='Research Fellow').exclude(alumni=False).count(),
		'fellows_oncourse': members.filter(position='Research Fellow').exclude(alumni=True).count(),
		'PhD_completed': publications.filter(pub_type='thesis', thesis_type='PhD').count(),
		'PhD_oncourse': members.filter(position='PhD Student').exclude(alumni=True).count(),
		'postdocs_completed': members.filter(position='PostDoc Researcher').exclude(alumni=False).count(),
		'postdocs_oncourse': members.filter(position='PostDoc Researcher').exclude(alumni=True).count(),
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
	alumni_postdocs = members.filter(alumni=True, position='PostDoc Researcher')
	alumni_phds = members.filter(alumni=True, position='PhD Student')
	alumni_fellows = members.filter(alumni=True, position='Research Fellow')
	alumni_masters = members.filter(alumni=True, position='MSc Student')
	alumni_undergraduates = members.filter(alumni=True, position='Undergraduate Students')
	
	context = {
		'page_title': 'People',
		'page_subtitle': 'PostDoc Fellows, PhD Students, Research Fellows, MSc Students and Undergradurate Students',
		'professors': professors,
		'postdocs': postdocs,
		'phds': phds,
		'fellows': fellows,
		'masters': masters,
		'undergraduates': undergraduates,
		'alumni_postdocs': alumni_postdocs,
		'alumni_phds': alumni_phds,
		'alumni_fellows': alumni_fellows,
		'alumni_masters': alumni_masters,
		'alumni_undergraduates': alumni_undergraduates,
	}
	return render(request, 'website/people.html', context)


def publications(request):
	publications = Publication.objects.all().order_by('-year', 'title')
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
		'current_year': datetime.datetime.today().year,
	}
	return render(request, 'website/publications.html', context)


def member_page(request, name_slug):

	try:
		member = Member.objects.get(slug=name_slug)
		names = member.name.split(' ')
		last_name = names[-1]
		initial = names[0][0] + '.'
		member_articles = Publication.objects.filter(pub_type='article', authors__contains=last_name).filter(authors__contains=initial).order_by('-year', 'title')
		member_book_chapters = Publication.objects.filter(pub_type='book-chapter', authors__contains=last_name).filter(authors__contains=initial).order_by('-year', 'title')
		member_patents = Publication.objects.filter(pub_type='patent', authors__contains=last_name).filter(authors__contains=initial).order_by('-year', 'title')
		member_posters = Publication.objects.filter(pub_type='poster', authors__contains=last_name).filter(authors__contains=initial).order_by('-year', 'title')
		member_presentations = Publication.objects.filter(pub_type='presentation', authors__contains=last_name).filter(authors__contains=initial).order_by('-year', 'title')
		member_theses = Publication.objects.filter(pub_type='thesis', authors__contains=last_name).filter(authors__contains=initial).order_by('-year', 'title')

		context = {
			'page_title': member.name,
			'page_subtitle': 'Personal Page',
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
		'page_subtitle': 'Research awards granted to members of the EgiChem group',
		'awards': awards,
	}	
	return render(request, 'website/awards.html', context)