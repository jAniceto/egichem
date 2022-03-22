from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Material, Announcement, ExternalResource, LabTeam, Faq

import csv
from datetime import datetime


def is_current_member(user):
    """Function to check if user is a current member (not alumni)"""
    try:
        if user.member:
            if user.member.alumni is False:
                print('Permission Granted.')
                return True
            else: 
                print('Permission Denied. Is Alumni.')
                return False

    except AttributeError as e:
        print('Permission denied.')
        return False


@user_passes_test(is_current_member)
def egichem(request):
    """Homepage for the private lab area"""
    announcements = Announcement.objects.all().order_by('-date_added')[:3]
    last_modified_material = Material.objects.all().order_by('-modified')[0]
    external_resources = ExternalResource.objects.all().order_by('order', 'date_added')

    context = {
		'page_title': 'Lab Home',
		'page_subtitle': '',
        'announcements': announcements,
        'last_modified_material': last_modified_material,
        'external_resources': external_resources
	}	
    return render(request, 'lab/home.html', context)


class MaterialListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    # permission_required = 'lab.manage_inventory'
    model = Material
    template_name = 'lab/inventory.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'materials'
    ordering = ['name']
    paginate_by = 100

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra context variables
        context['page_title'] = 'inventory'
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(name__icontains=query) | 
                Q(specifications__icontains=query) |
                Q(item_type__icontains=query)
            ).distinct().order_by('name')
        else:
            object_list = self.model.objects.all().order_by('name')
        return object_list


class MaterialCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Material
    fields = ['item_type', 'name', 'specifications', 'amount', 'location', 'comments']

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MaterialUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Material
    fields = ['item_type', 'name', 'cas', 'specifications', 'amount', 'location', 'comments']

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MaterialDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('inventory')

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False


class AnnouncementListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    # permission_required = 'lab.manage_inventory'
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'lab/announcements.html'  # <app>/<model>_<viewtype>.html
    ordering = ['-date_added']

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra context variables
        context['page_title'] = 'announcements'
        return context


class AnnouncementCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Announcement
    fields = ['title', 'content']

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@user_passes_test(is_current_member)
def announcement_delete(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    return redirect('announcements')


@user_passes_test(is_current_member)
def export(request):
    """Exports inventory list to CSV"""
    materials = Material.objects.all()

    material_list = []
    for material in materials:
        material_list.append({
            'item_type': material.item_type,
            'name': material.name,
            'specifications': material.specifications,
            'amount': material.amount,
            'location': material.location,
            'comments': material.comments.replace('\r\n', ', '),
            'created': material.created,
            'modified': material.modified,
            'last_modified_by': material.user,
        })
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    # Create CSV file
    fnames = ['item_type', 'name', 'specifications', 'amount', 'location', 'comments', 'created', 'modified', 'last_modified_by']
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.DictWriter(response, fieldnames=fnames)
    writer.writeheader()  # writes the headers to the CSV file.
    for material in material_list:
        writer.writerow(material)

    return response


class FaqListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Faq
    context_object_name = 'faqs'
    template_name = 'lab/faq.html'  # <app>/<model>_<viewtype>.html
    ordering = ['order', 'date_added']

    def test_func(self):
        try:
            if self.request.user.member:
                if self.request.user.member.alumni is False:
                    return True
                else: 
                    return False
        except AttributeError as e:
            return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra context variables
        context['page_title'] = 'faqs'
        return context


@user_passes_test(is_current_member)
def lab_teams(request):
    """Lab teams page"""
    
    def create_teams(teams):
        current_month = datetime.now().month
        current_year = datetime.now().year

        current_found = False
        cleaning_members, technic_members, safety_members = None, None, None
        for team in teams:
            if (team.year == current_year) and (team.month == current_month) and current_found == False:
                if not cleaning_members:
                    cleaning_members = team.cleaning.all()
                if not technic_members:
                    technic_members = team.technic.all()
                if not safety_members:
                    safety_members = team.safety.all()
                current_found = True
            
            elif current_found:
                if not cleaning_members:
                    cleaning_members = team.cleaning.all()
                if not technic_members:
                    technic_members = team.technic.all()
                if not safety_members:
                    safety_members = team.safety.all()
                    current_found = True
        return cleaning_members, technic_members, safety_members

    teams = LabTeam.objects.all().order_by('-year', '-month')
    cleaning_members, technic_members, safety_members = create_teams(teams)

    context = {
		'page_title': 'lab_teams',
		'page_subtitle': '',
        'teams': teams,
        'cleaning_members': cleaning_members,
        'technic_members': technic_members,
        'safety_members': safety_members,
	}	
    return render(request, 'lab/lab_teams.html', context)
