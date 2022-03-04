from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='form')),
    path('form', views.form, name='form'),
    path('detail', views.detail, name='detail')
]
