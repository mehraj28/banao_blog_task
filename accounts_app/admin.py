from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BlogPost, Appointment, Category


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'address_line1', 'city', 'state', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_patient', 'is_doctor')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def view_patients(self, request, queryset):
        return queryset.filter(is_patient=True)

    def view_doctors(self, request, queryset):
        return queryset.filter(is_doctor=True)


admin.site.register(BlogPost)
admin.site.register(Appointment)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
