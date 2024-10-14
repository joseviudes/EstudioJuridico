from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'username', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permisos', {'fields': ('rol', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'fecha_ingreso')}),
    )
    
    # 'fecha_ingreso' es de solo lectura
    readonly_fields = ('fecha_ingreso',)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'rol', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(Usuario, UsuarioAdmin)
