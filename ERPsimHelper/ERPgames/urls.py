from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index')
    # path('', RedirectView.as_view(url='form')),
    # path('form', views.form, name='form'),
    # path('detail', views.detail, name='detail')
]