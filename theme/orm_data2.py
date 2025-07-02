import os

def pausar_y_limpiar():
    input("Presione una tecla para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

# ======================================
# IMPORTAR MODELOS Y DEPENDENCIAS DJANGO
# ======================================
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from security.models import Menu, Module, GroupModulePermission

# ======================================
# 1. CREAR MENÚS PRINCIPALES DEL SISTEMA
# ======================================
# ORM shell_plus:
# menu = Menu.objects.create(name='Pacientes', icon='bi bi-people-fill', order=1)
menus_data = [
    {"name": "Pacientes",     "icon": "bi bi-people-fill",       "order": 1},
    {"name": "Citas",         "icon": "bi bi-calendar-event",    "order": 2},
    {"name": "Consultas",     "icon": "bi bi-clipboard-heart",   "order": 3},
    {"name": "Farmacia",      "icon": "bi bi-capsule",           "order": 4},
    {"name": "Reportes",      "icon": "bi bi-bar-chart",         "order": 5},
    {"name": "Usuarios",      "icon": "bi bi-person-badge",      "order": 6},
]
menus_obj = []
for m in menus_data:
    menu = Menu.objects.create(**m)
    menus_obj.append(menu)
menu_dict = {m.name: m for m in menus_obj}
print("==== MENÚS CREADOS ====")
for m in menus_obj:
    print(f"- {m.name}")
pausar_y_limpiar()

# ======================================
# 2. CREAR MÓDULOS POR MENÚ
# ======================================
# ORM shell_plus:
# modulo = Module.objects.create(url='pacientes/', name='Gestión de Pacientes', menu=Menu.objects.get(name='Pacientes'))
modulos_data = [
    # Pacientes
    {"url": "pacientes/",             "name": "Gestión de Pacientes",   "menu": "Pacientes",  "description": "Registro y control de pacientes",     "icon": "bi bi-person-vcard",      "order": 1},
    # Citas
    {"url": "citas/",                 "name": "Gestión de Citas",       "menu": "Citas",      "description": "Agendamiento y control de citas",     "icon": "bi bi-calendar-plus",     "order": 1},
    # Consultas
    {"url": "consultas/",             "name": "Consultas Médicas",      "menu": "Consultas",  "description": "Registro de consultas médicas",       "icon": "bi bi-clipboard2-pulse",  "order": 1},
    # Farmacia
    {"url": "medicamentos/",          "name": "Medicamentos",           "menu": "Farmacia",   "description": "Gestión de medicamentos",             "icon": "bi bi-capsule",           "order": 1},
    {"url": "stock_farmacia/",        "name": "Stock de Farmacia",      "menu": "Farmacia",   "description": "Inventario de farmacia",              "icon": "bi bi-box-seam",          "order": 2},
    # Reportes
    {"url": "reportes/atencion/",     "name": "Reporte de Atenciones",  "menu": "Reportes",   "description": "Reporte de atenciones médicas",       "icon": "bi bi-clipboard-data",     "order": 1},
    {"url": "reportes/medicamentos/", "name": "Reporte de Medicamentos","menu": "Reportes",   "description": "Reporte de medicamentos",             "icon": "bi bi-capsule-pill",       "order": 2},
    # Usuarios
    {"url": "usuarios/",              "name": "Gestión de Usuarios",    "menu": "Usuarios",   "description": "Administración de usuarios",          "icon": "bi bi-person-lines-fill",  "order": 1},
    {"url": "roles/",                 "name": "Roles y Permisos",       "menu": "Usuarios",   "description": "Administración de roles y permisos",  "icon": "bi bi-shield-lock",        "order": 2},
]
modulos_obj = []
for m in modulos_data:
    modulo = Module.objects.create(
        url=m["url"],
        name=m["name"],
        menu=menu_dict[m["menu"]],
        description=m["description"],
        icon=m["icon"],
        order=m["order"],
        is_active=True
    )
    modulos_obj.append(modulo)
module_dict = {m.name: m for m in modulos_obj}
print("==== MÓDULOS CREADOS ====")
for m in modulos_obj:
    print(f"- {m.name} ({m.menu.name})")
pausar_y_limpiar()

# ======================================
# 3. CREAR GRUPOS/ROLES
# ======================================
# ORM shell_plus:
# grupo = Group.objects.create(name='Médicos')
grupos_data = ["Administradores", "Médicos", "Enfermeros", "Farmacéuticos", "Recepcionistas"]
grupos_obj = []
for nombre in grupos_data:
    grupo = Group.objects.create(name=nombre)
    grupos_obj.append(grupo)
group_dict = {g.name: g for g in grupos_obj}
print("==== GRUPOS CREADOS ====")
for g in grupos_obj:
    print(f"- {g.name}")
pausar_y_limpiar()

# ======================================
# 4. CREAR USUARIOS DE EJEMPLO
# ======================================
# ORM shell_plus:
# User = get_user_model()
# user = User.objects.create_user(email='admin@demo.com', password='admin123', first_name='Admin', last_name='Demo')
User = get_user_model()
usuarios = [
    {"username": "admin",        "email": "admin@demo.com",        "password": "admin123",    "first_name": "Admin",      "last_name": "Principal"},
    {"username": "medico1",      "email": "medico1@demo.com",      "password": "med123",      "first_name": "Gregory",    "last_name": "House"},
    {"username": "enfermera1",   "email": "enfermera1@demo.com",   "password": "enf123",      "first_name": "Ana",        "last_name": "Cruz"},
    {"username": "farmaceutico1","email": "farmaceutico1@demo.com","password": "farm123",     "first_name": "Maria",      "last_name": "Botica"},
    {"username": "recep1",       "email": "recep1@demo.com",       "password": "recep123",    "first_name": "Juan",       "last_name": "Frontdesk"},
]
usuarios_obj = []
for u in usuarios:
    user = User.objects.create_user(
        username=u["username"],
        email=u["email"],
        password=u["password"],
        first_name=u["first_name"],
        last_name=u["last_name"]
    )
    usuarios_obj.append(user)
print("==== USUARIOS CREADOS ====")
for u in usuarios:
    print(f"- {u['username']} ({u['email']})")
pausar_y_limpiar()

# ======================================
# 5. CREAR Y ASOCIAR PERMISOS A CADA MÓDULO
# ======================================
# ORM shell_plus:
# from django.contrib.contenttypes.models import ContentType
# ct = ContentType.objects.get_for_model(Module)
# permiso = Permission.objects.create(codename='add_gestion_de_pacientes', name='Puede agregar pacientes', content_type=ct)
# modulo.permissions.add(permiso)
ct = ContentType.objects.get_for_model(Module)
permisos_base = [
    {"codename": "add",     "name": "Puede agregar"},
    {"codename": "change",  "name": "Puede modificar"},
    {"codename": "delete",  "name": "Puede eliminar"},
    {"codename": "view",    "name": "Puede ver"},
]
perm_objs = {}  # {(modulo, codename): permission}
for modulo in modulos_obj:
    for perm in permisos_base:
        codename = f"{perm['codename']}_{modulo.name.lower().replace(' ', '_')}"
        name = f"{perm['name']} {modulo.name}"
        permiso, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=ct
        )
        modulo.permissions.add(permiso)
        perm_objs[(modulo.name, perm['codename'])] = permiso
print("==== PERMISOS GENERADOS Y ASIGNADOS ====")
for modulo in modulos_obj:
    print(f"- {modulo.name}: {[p.codename for p in modulo.permissions.all()]}")
pausar_y_limpiar()

# ======================================
# 6. ASIGNAR PERMISOS A GRUPOS EN CADA MÓDULO
# ======================================
# ORM shell_plus:
# gmp = GroupModulePermission.objects.create(group=grupo, module=modulo)
# gmp.permissions.add(permiso1, permiso2, ...)
# --- Administradores: todos los permisos ---
for modulo in modulos_obj:
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Administradores"], module=modulo)
    gmp.permissions.set(modulo.permissions.all())

# --- Médicos: ver y editar pacientes, citas, consultas; solo ver farmacia y reportes ---
for modulo_name in ["Gestión de Pacientes", "Gestión de Citas", "Consultas Médicas"]:
    modulo = module_dict[modulo_name]
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Médicos"], module=modulo)
    # Todos menos delete
    gmp.permissions.set([perm for cod, perm in perm_objs.items() if cod[0] == modulo.name and cod[1] in ("add", "change", "view")])
for modulo_name in ["Medicamentos", "Stock de Farmacia", "Reporte de Atenciones", "Reporte de Medicamentos"]:
    modulo = module_dict[modulo_name]
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Médicos"], module=modulo)
    gmp.permissions.set([perm_objs[(modulo.name, "view")]])

# --- Enfermeros: solo ver pacientes, citas, consultas; cambiar stock de farmacia ---
for modulo_name in ["Gestión de Pacientes", "Gestión de Citas", "Consultas Médicas"]:
    modulo = module_dict[modulo_name]
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Enfermeros"], module=modulo)
    gmp.permissions.set([perm_objs[(modulo.name, "view")]])
modulo = module_dict["Stock de Farmacia"]
gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Enfermeros"], module=modulo)
gmp.permissions.set([perm_objs[(modulo.name, "change")]])

# --- Farmacéuticos: todos los permisos en farmacia, ver reportes de medicamentos ---
for modulo_name in ["Medicamentos", "Stock de Farmacia"]:
    modulo = module_dict[modulo_name]
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Farmacéuticos"], module=modulo)
    gmp.permissions.set(modulo.permissions.all())
modulo = module_dict["Reporte de Medicamentos"]
gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Farmacéuticos"], module=modulo)
gmp.permissions.set([perm_objs[(modulo.name, "view")]])

# --- Recepcionistas: ver/agregar pacientes y citas, ver reportes ---
for modulo_name in ["Gestión de Pacientes", "Gestión de Citas"]:
    modulo = module_dict[modulo_name]
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Recepcionistas"], module=modulo)
    permisos = [perm_objs[(modulo.name, "add")], perm_objs[(modulo.name, "view")]]
    gmp.permissions.set(permisos)
for modulo_name in ["Reporte de Atenciones", "Reporte de Medicamentos"]:
    modulo = module_dict[modulo_name]
    gmp, _ = GroupModulePermission.objects.get_or_create(group=group_dict["Recepcionistas"], module=modulo)
    gmp.permissions.set([perm_objs[(modulo.name, "view")]])
print("==== PERMISOS ASIGNADOS A GRUPOS EN CADA MÓDULO ====")
pausar_y_limpiar()

# ======================================
# 7. ASIGNAR USUARIOS A GRUPOS
# ======================================
# ORM shell_plus:
# user.groups.add(grupo)
usuarios_grupos = [
    (0, 0),  # admin -> Administradores
    (1, 1),  # medico1 -> Médicos
    (2, 2),  # enfermera1 -> Enfermeros
    (3, 3),  # farmaceutico1 -> Farmacéuticos
    (4, 4),  # recep1 -> Recepcionistas
]
for usuario_idx, grupo_idx in usuarios_grupos:
    usuarios_obj[usuario_idx].groups.add(grupos_obj[grupo_idx])
print("==== USUARIOS ASIGNADOS A SUS GRUPOS ====")
for idx, (u, g) in enumerate(usuarios_grupos):
    print(f"- {usuarios_obj[u].username} => {grupos_obj[g].name}")
pausar_y_limpiar()

print("¡Sistema de seguridad MÉDICO con datos creados exitosamente! :)")
# ======================================