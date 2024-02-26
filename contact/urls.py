from django.urls import path
from . import views
app_name = 'contact'

urlpatterns = [
    # CRUD
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'),  # delete
    path('contact/<int:contact_id>/update/', views.update, name='update'),  # update
    path('contact/<int:contact_id>/', views.contact, name='contact'),  # read
    path('contact/create/', views.create, name='create'),  # create
    # busca
    path('search/', views.search, name='search'),
    # home
    path('', views.index, name='index'),
]
