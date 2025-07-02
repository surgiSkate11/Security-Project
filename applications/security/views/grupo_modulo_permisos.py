# Vistas para el manejo de grupos, módulos y permisos de seguridad

from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.group_module_permisos import GroupModulePermissionForm
from applications.security.models import GroupModulePermission
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from applications.security.models import Module
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/grupos_modulos_permisos/list.html'
    model = GroupModulePermission
    context_object_name = 'GroupModulePermissions'
    permission_required = 'view_groupmodulepermission'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(group__name__icontains=q1), Q.OR)
            self.query.add(Q(module__name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        print(context['permissions'])
        return context


class GroupModulePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GroupModulePermission
    template_name = 'security/grupos_modulos_permisos/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'add_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Grupo Módulo Permiso'
        context['back_url'] = self.success_url
        
        
        # Obtener todos los datos necesarios para la página dinámica
        all_groups = Group.objects.all()
        all_modules = Module.objects.all()
        existing_assignments = GroupModulePermission.objects.select_related('group', 'module').prefetch_related('permissions').all()
        
        # Datos para los acordeones dinámicos
        groups_data = []
        for group in all_groups:
            # Obtener módulos ya asignados a este grupo
            assigned_modules = set(existing_assignments.filter(group=group).values_list('module_id', flat=True))
            
            # Módulos disponibles (no asignados)
            available_modules = [
                {"id": m.id, "name": m.name, "icon": m.icon} 
                for m in all_modules if m.id not in assigned_modules
            ]
            
            groups_data.append({
                "id": group.id,
                "name": group.name,
                "available_modules": available_modules
            })
        
        # Relación módulo → permisos
        module_permissions = {}
        for module in all_modules:
            perms = module.permissions.all()
            module_permissions[module.id] = [
                {"id": p.id, "name": p.name, "codename": p.codename} for p in perms
            ]
          # Asignaciones recientes de la sesión (solo las que el usuario ha creado en esta sesión
        
        context.update({
            "groups_data": json.dumps(groups_data),
            "module_permissions": json.dumps(module_permissions),
            "all_groups": all_groups,
            "all_modules": all_modules
        })
        
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo_modulo_permiso = self.object
        messages.success(self.request, f"Éxito al crear el grupo módulo permiso {grupo_modulo_permiso.id}.")
        return response



class GroupModulePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GroupModulePermission
    template_name = 'security/grupos_modulos_permisos/form_update.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'change_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Grupo Módulo Permiso'
        context['back_url'] = self.success_url

        module_perms = set(self.object.module.permissions.all())
        assigned_perms = set(self.object.permissions.all())
        combined_perms = list(module_perms.union(assigned_perms))
        context['combined_permissions'] = combined_perms

        if self.request.method == "POST":
            context["selected_permissions"] = self.request.POST.getlist("permissions[]")
        else:
            context["selected_permissions"] = [str(p.id) for p in self.object.permissions.all()]
        return context

    def post(self, request, *args, **kwargs):
        """Override post method to handle permissions update"""
        self.object = self.get_object()
        
        # Obtener los IDs de permisos seleccionados
        permission_ids = request.POST.getlist("permissions[]")
        
        try:
            # Actualizar los permisos
            self.object.permissions.set(permission_ids)
            
            # Mensaje de éxito
            messages.success(
                request,
                f"Permisos actualizados correctamente para {self.object.group.name} - {self.object.module.name}."
            )
            
            # Redirigir al success_url
            return HttpResponseRedirect(self.success_url)
            
        except Exception as e:
            # En caso de error, mostrar mensaje y recargar el formulario
            messages.error(request, f"Error al actualizar permisos: {str(e)}")
            return self.get(request, *args, **kwargs)
      

class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = 'core/delete.html'
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = 'delete_groupmodulepermission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Grupo Módulo Permiso'
        context['description'] = f"¿Desea eliminar el grupo módulo permiso: {self.object.id}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        group_module_permission = self.object
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar el grupo módulo permiso {group_module_permission.id}.")

        return response


@method_decorator(csrf_exempt, name='dispatch')
class GroupModulePermissionAjaxView(PermissionMixin, View):
    permission_required = 'add_groupmodulepermission'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            assignments = data.get('assignments', [])
            if not assignments:
                return JsonResponse({'success': False, 'message': 'No se recibieron asignaciones.'})

            messages = []
            for item in assignments:
                group_id = item.get('group_id')
                module_id = item.get('module_id')
                permission_ids = item.get('permission_ids', [])

                if not group_id or not module_id or not permission_ids:
                    continue

                try:
                    group = Group.objects.get(id=group_id)
                    module = Module.objects.get(id=module_id)
                    permissions = Permission.objects.filter(id__in=permission_ids)
                except:
                    continue

                existing = GroupModulePermission.objects.filter(group=group, module=module).first()
                if existing:
                    messages.append(f"Ya existe: {group.name} - {module.name}")
                    continue

                assignment = GroupModulePermission.objects.create(group=group, module=module)
                assignment.permissions.set(permissions)
                messages.append(f"Creado: {group.name} - {module.name}")

            return JsonResponse({'success': True, 'message': " | ".join(messages)})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'})
