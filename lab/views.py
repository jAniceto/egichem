from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Material


class MaterialListView(LoginRequiredMixin, ListView):
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

# def inventory(request):
#     materials = Material.objects.all().order_by('name')
#     context = {
#         'page_title': 'inventory',
#         'materials': materials,
#         }	
#     return render(request, 'lab/inventory.html', context)