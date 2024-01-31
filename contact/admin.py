from django.contrib import admin
# Register your models here.
from contact import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = '-id',


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email',)
    ordering = '-id',  # ordena de modo decrescente, crescente -> id
    search_fields = 'first_name', 'last_name', 'phone', 'email',
    list_per_page = 20
    list_max_show_all = 200
    list_editable = 'phone', 'email',
    list_display_links = 'first_name', 'last_name',  # nãp pode ter valores de list_editable
