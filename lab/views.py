from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Material, Announcement


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


class MaterialListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    # permission_required = 'lab.manage_inventory'
    model = Material
    template_name = 'lab/inventory.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'materials'
    ordering = ['name']
    paginate_by = 25

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
                Q(specifications__icontains=query)
            ).distinct().order_by('name')
        else:
            object_list = self.model.objects.all().order_by('name')
        return object_list


class MaterialCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Material
    fields = ['name', 'specifications', 'amount', 'location', 'comments']

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
    fields = ['name', 'cas', 'specifications', 'amount', 'location', 'comments']

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
def egichem(request):

    announcements = Announcement.objects.all().order_by('-date_added')[:3]

    context = {
		'page_title': 'Lab Home',
		'page_subtitle': 'test',
        'announcements': announcements,
	}	
    return render(request, 'lab/home.html', context)