from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin # UserAdmin is a built-in class in Django
from django.contrib.auth.models import User, Group
# Register your models here.

admin.site.unregister(User) # Unregister User model to prevent editing of User model from admin panel
admin.site.unregister(Group) # Unregister Group model to prevent editing of Group model from admin panel

@admin.register(User) # Customizing the User model instead of using the built-in User model
class CustomUserAdmin(UserAdmin): # This is useful when you want to add more fields to the User model and also to prevent non-superusers from editing certain fields
    # Overriding get_form method to prevent non-superusers from editing certain fields
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields["username"].disabled = True
            form.base_fields["is_superuser"].disabled = True
            form.base_fields["user_permissions"].disabled = True # Disable non-superuser such as staff from editing user permissions
            form.base_fields["groups"].disabled = True # Disable non-superuser such as staff from editing user groups
        return form

# class ReadOnlyAdminMixin: # WARNING: Python is top-down approach so if you want to inherit a class, it must be defined first unlike Java
#     def has_add_permission(self, request):
#         if request.user.has_perm('inventory.add_product'):
#             return True
#         else:
#             return False
#
#     def has_change_permission(self, request, obj=None):
#         # To identify the perm name, go to django_content_type table and check the name of the model you want to restrict
#         # Go to auth_permission table and check the codename of the permission you want to restrict
#         if request.user.has_perm('inventory.change_product'):
#             return True
#         else:
#             return False
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def has_view_permission(self, request, obj=None):
#         return True
# @admin.register(Product) # Alternative for admin.site.register(Product)
# class ProductAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
#     list_display = ['name']
#
#     # override get_form method (by restricting some form fields) to prevent non-superusers from editing certain fields
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser # user has a is_superuser attribute (check auth_user table)
#
#         if not is_superuser:
#             form.base_fields["web_id"].disabled = True
#             form.base_fields["slug"].disabled = True
#             form.base_fields["name"].disabled = True
#         return form
#
#     # overriding permissions (to know what method to override go to auth_permission table and
#     # check the codename of the permission you want to override)


