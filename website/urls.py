from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('research/', views.research, name='research'),
    path('people/', views.people, name='people'),
    # path('lab/', views.lab, name='lab'),
    path('publications/', views.publications, name='publications'),
    path('partners/', views.partners, name='partners'),
    # path('news/', views.news, name='news'),  # handled via blog app
    path('tools/', views.tools, name='tools'),
    # path('contact/', views.contact, name='contact'),  # handled via sendemail app
    path('awards/', views.awards, name='awards'),
    path('people/<slug:name_slug>/', views.member_page, name='member_page'),
]
