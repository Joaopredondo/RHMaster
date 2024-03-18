from django.shortcuts import render
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView,
    DeleteView
)
from .models import Departamento
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class DepartamentosList(ListView):
    model = Departamento

@method_decorator(login_required, name='dispatch')
class DepartamentosCreate(CreateView):
    model = Departamento
    fields = ['nome']

    def form_valid(self, form):
        departamento = form.save(commit=False)
        departamento.empresa = self.request.user.funcionario.empresas
        departamento.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DepartamentosEdit(UpdateView):
    model = Departamento
    fields = ['nome']

@method_decorator(login_required, name='dispatch')
class DepartamentosDelete(DeleteView):
    model = Departamento
    success_url = reverse_lazy('list_departamentos')
