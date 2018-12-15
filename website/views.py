from django.shortcuts import render
from .models import ResearchField


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