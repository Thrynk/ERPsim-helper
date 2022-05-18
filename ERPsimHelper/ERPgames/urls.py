from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', views.index, name='index')
    # path('', RedirectView.as_view(url='form')),
    # path('form', views.form, name='form'),
    # path('detail', views.detail, name='detail')
]