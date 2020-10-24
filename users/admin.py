from django.contrib import admin
from .models import Customer, Courrier, Supplier, User
# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('county'),
@admin.register(Courrier)
class CourrierAdmin(admin.ModelAdmin):
    pass
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Customer)
# admin.site.register(Courrier)
# admin.site.register(Supplier)
# admin.site.register(User)