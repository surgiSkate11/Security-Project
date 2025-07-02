from django.urls import path

from applications.doctor.views.patient import PatientListView, PatientCreateView, PatientUpdateView, PatientDeleteView

app_name = 'doctor'

urlpatterns = [
    # rutas de pacientes
    path('patient_list/', PatientListView.as_view(), name="patient_list"),
    path('patient_create/', PatientCreateView.as_view(), name="patient_create"),
    path('patient_update/<int:pk>/', PatientUpdateView.as_view(), name="patient_update"),
    path('patient_delete/<int:pk>/', PatientDeleteView.as_view(), name="patient_delete"),
]