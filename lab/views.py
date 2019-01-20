from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Material


class MaterialListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'lab.manage_inventory'
    model = Material
    template_name = 'lab/inventory.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'materials'
    ordering = ['name']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in extra context variables
        context['page_title'] = 'inventory'
        return context


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
