from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.doctor.forms.patient import PatientForm
from applications.doctor.models import Patient
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class PatientListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/pacientes/list.html'
    model = Patient
    context_object_name = 'patients'
    permission_required = 'view_patient'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(first_name__icontains=q1), Q.OR)
            self.query.add(Q(last_name__icontains=q1), Q.OR)
            self.query.add(Q(dni__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:patient_create')
        return context

class PatientCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Patient
    template_name = 'doctor/pacientes/form.html'
    form_class = PatientForm
    success_url = reverse_lazy('doctor:patient_list')
    permission_required = 'add_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Paciente'
        context['back_url'] = self.success_url
        context['title1'] = 'Nuevo Paciente'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        patient = self.object
        messages.success(self.request, f"Éxito al crear el paciente {patient.first_name} {patient.last_name}.")
        return response

class PatientUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Patient
    template_name = 'doctor/pacientes/form.html'
    form_class = PatientForm
    success_url = reverse_lazy('doctor:patient_list')
    permission_required = 'change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        context['title1'] = 'Editar Paciente'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        patient = self.object
        messages.success(self.request, f"Éxito al actualizar el paciente {patient.first_name} {patient.last_name}.")
        return response

class PatientDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Patient
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:patient_list')
    permission_required = 'delete_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar el paciente: {self.object.first_name} {self.object.last_name}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        patient_name = f"{self.object.first_name} {self.object.last_name}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar lógicamente el paciente {patient_name}.")
        return response