from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Material, Announcement


class MaterialListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'lab.manage_inventory'
    model = Material
    template_name = 'lab/inventory.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'materials'
    ordering = ['name']
    paginate_by = 25

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
                Q(specifications__icontains=query)
            ).distinct().order_by('name')
        else:
            object_list = self.model.objects.all().order_by('name')
        return object_list


class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    fields = ['name', 'specifications', 'amount', 'location', 'comments']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = Material
    fields = ['name', 'cas', 'specifications', 'amount', 'location', 'comments']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('inventory')


class AnnouncementListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'lab.manage_inventory'
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'lab/announcements.html'  # <app>/<model>_<viewtype>.html
    ordering = ['-date_added']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra context variables
        context['page_title'] = 'announcements'
        return context


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def announcement_delete(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    return redirect('announcements')


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
def our_lab(request):

    announcements = Announcement.objects.all().order_by('-date_added')[:3]

    context = {
		'page_title': 'Lab Home',
		'page_subtitle': 'test',
        'announcements': announcements,
	}	
    return render(request, 'lab/home.html', context)