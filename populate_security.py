import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_clinico.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from applications.security.models import Menu, Module, User, GroupModulePermission

# Crear Menús
menus = [
    {'name': 'Administración', 'icon': 'bi bi-gear', 'order': 1},
    {'name': 'Pacientes', 'icon': 'bi bi-person', 'order': 2},
    {'name': 'Doctores', 'icon': 'bi bi-heart-pulse', 'order': 3},
]
menu_objs = [Menu.objects.create(**m) for m in menus]

# Crear Módulos
modules = [
    {'url': 'usuarios/', 'name': 'Usuarios', 'menu': menu_objs[0], 'description': 'Gestión de usuarios', 'icon': 'bi bi-people', 'order': 1},
    {'url': 'grupos/', 'name': 'Grupos', 'menu': menu_objs[0], 'description': 'Gestión de grupos', 'icon': 'bi bi-people-fill', 'order': 2},
    {'url': 'modulos/', 'name': 'Módulos', 'menu': menu_objs[0], 'description': 'Gestión de módulos', 'icon': 'bi bi-box', 'order': 3},
    {'url': 'pacientes/', 'name': 'Pacientes', 'menu': menu_objs[1], 'description': 'Gestión de pacientes', 'icon': 'bi bi-person', 'order': 1},
    {'url': 'historial/', 'name': 'Historial', 'menu': menu_objs[1], 'description': 'Historial médico', 'icon': 'bi bi-journal-medical', 'order': 2},
    {'url': 'doctores/', 'name': 'Doctores', 'menu': menu_objs[2], 'description': 'Gestión de doctores', 'icon': 'bi bi-heart-pulse', 'order': 1},
    {'url': 'especialidades/', 'name': 'Especialidades', 'menu': menu_objs[2], 'description': 'Gestión de especialidades', 'icon': 'bi bi-star', 'order': 2},
]
module_objs = [Module.objects.create(**m) for m in modules]

# Crear Grupos
grupo_admin, _ = Group.objects.get_or_create(name='Administradores')
grupo_doctor, _ = Group.objects.get_or_create(name='Doctores')
grupo_paciente, _ = Group.objects.get_or_create(name='Pacientes')
grupo_secretaria, _ = Group.objects.get_or_create(name='Secretarias')

# Crear Usuarios
usuarios = [
    {'email': 'admin@demo.com', 'username': 'admin', 'first_name': 'Admin', 'last_name': 'Demo', 'password': 'admin123', 'is_superuser': True, 'is_staff': True},
    {'email': 'doctor1@demo.com', 'username': 'doctor1', 'first_name': 'Juan', 'last_name': 'Pérez', 'password': 'doctor123'},
    {'email': 'doctor2@demo.com', 'username': 'doctor2', 'first_name': 'Ana', 'last_name': 'García', 'password': 'doctor123'},
    {'email': 'paciente1@demo.com', 'username': 'paciente1', 'first_name': 'Carlos', 'last_name': 'López', 'password': 'paciente123'},
    {'email': 'paciente2@demo.com', 'username': 'paciente2', 'first_name': 'María', 'last_name': 'Martínez', 'password': 'paciente123'},
    {'email': 'secretaria1@demo.com', 'username': 'secretaria1', 'first_name': 'Lucía', 'last_name': 'Vega', 'password': 'secretaria123'},
]
user_objs = []
for u in usuarios:
    user = User.objects.create_user(
        email=u['email'], username=u['username'], first_name=u['first_name'], last_name=u['last_name'], password=u['password']
    )
    if u.get('is_superuser'):
        user.is_superuser = True
        user.is_staff = True
        user.save()
    user_objs.append(user)

# Asignar usuarios a grupos
user_objs[0].groups.add(grupo_admin)
user_objs[1].groups.add(grupo_doctor)
user_objs[2].groups.add(grupo_doctor)
user_objs[3].groups.add(grupo_paciente)
user_objs[4].groups.add(grupo_paciente)
user_objs[5].groups.add(grupo_secretaria)

# Asignar módulos a grupos (ejemplo simple)
for module in module_objs:
    GroupModulePermission.objects.get_or_create(group=grupo_admin, module=module)
    if module.menu.name == 'Doctores':
        GroupModulePermission.objects.get_or_create(group=grupo_doctor, module=module)
    if module.menu.name == 'Pacientes':
        GroupModulePermission.objects.get_or_create(group=grupo_paciente, module=module)

print('¡Datos de ejemplo cargados exitosamente!')
