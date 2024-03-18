from django.http import HttpResponse
from django.views.generic import (
    ListView, 
    UpdateView, 
    DeleteView, 
    CreateView
)
from .models import Funcionario
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class FuncionarioCreate(CreateView):
    model = Funcionario
    fields = ['nome', 'Departamentos']

    def form_valid(self, form):
        funcionario = form.save(commit=False)
        username = funcionario.nome.split(' ')[0] + funcionario.nome.split(' ')[1]
        funcionario.empresas = self.request.user.funcionario.empresas
        funcionario.user = User.objects.create(username=username)
        funcionario.save()
        return super(FuncionarioCreate, self).form_valid(form)

class FuncionariosList(ListView):
    model = Funcionario

    def get_queryset(self):
        # Verifique se o usuário logado tem um funcionário associado antes de acessar os funcionários
        if hasattr(self.request.user, 'funcionario'):
            empresa_logada = self.request.user.funcionario.empresas
            queryset = Funcionario.objects.filter(empresas=empresa_logada)
            return queryset
        else:
            # Lide com o caso em que o usuário não tem um funcionário associado
            return Funcionario.objects.none()

class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'Departamentos']

class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('list_funcionarios')
