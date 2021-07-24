from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
)
#Models
from . models import Empleado
#forms
from .forms import EmpleadoForm

class InicioView(TemplateView):
    """ Vista que carga la pagina de inicio"""
    template_name = 'inicio.html'

class ListAllEmpleados(ListView):
    template_name = 'persona/list_all.html'
    paginate_by = 4
    ordering = 'first_name'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('**************')
        palabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            full_name__icontains=palabra_clave
        )
        return lista

class ListEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'
    model = Empleado


class ListByAreaEmpleado(ListView):
    """ lista empleados de un area """
    template_name = 'persona/list_by_area.html'
    context_object_name = 'empleados'
    
    def get_queryset(self):
        #el codigo que yo quiera
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(
            departamento__shor_name=area
        )
        return lista
        

class ListByJobEmpleado(ListView):
    """ lista empleados de un Trabajo """
    template_name = 'persona/list_by_job.html'
    context_object_name = 'empleados'
    ordering = 'job'

    def get_queryset(self):
        #el codigo que yo quiera
        trabajo = 'informatica'
        lista = Empleado.objects.filter(job=trabajo)
        return lista

class ListEmpleadosByKword(ListView):
    """ lista empleado por palabra clave"""
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('**************')
        palabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            first_name=palabra_clave
        )
        return lista


class ListaHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        empleado = Empleado.objects.get(id=1)
        return empleado.habilidades.all()

class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/detail_empleado.html"

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        #todo el contexto
        context['titulo'] = 'Empleado del mes'
        return context

class SuccessView(TemplateView):
    template_name = "persona/success.html"


class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'persona/add.html'
    form_class = EmpleadoForm
    #Esencial tenir un fields en createview, son es attributs que ens sortira per pantalla
    #fields = ('__all__') 
    #per posar tots es camps des model empleado.
    success_url = reverse_lazy('persona_app:empleados_admin')
    def form_valid(self, form):
        #logica del proceso
        empleado = form.save(commit=False) #tot lu des form_valid s'almacena dins aquesta variable
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = "persona/update.html"
    fields = [
        'first_name',
        'last_name',
        'job', 
        'departamento',
        'habilidades',
        'avatar',
    ]
    success_url = reverse_lazy('persona_app:empleados_admin')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('***************METODO POST**************')
        print('**********************************')
        print(request.POST)
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        #logica del proceso
        print('***************METODO form valid**************')
        print('**********************************')
        return super(EmpleadoUpdateView, self).form_valid(form)
 
class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "persona/delete.html"
    success_url = reverse_lazy('persona_app:empleados_admin')

# Create your views here.
# 1.- Listar todos los empleados de la empresa
# 2.- Listar todos los empleados que pertenecen a una area de la empresa
# 3.- Listar empleados por trabajo
# 4.- Listar los empleados por palabra clave
# 5.- Listar habilidades de un empleado