from django.views.generic import TemplateView
from django.urls import path, include
from django.contrib import admin

from . import view

urlpatterns = [
    # admin panel
    path('admin/', admin.site.urls),
    
    # react landing page
    path('react/', TemplateView.as_view(template_name="index.html")),
    
    # authentication view functions
    path('login/', view.login),
    path("sign-up/", view.signup),
    path("log-out/", view.logout),
    
    # payment view functions
    path("payment-page/", view.index, name="index"),
    path("charge/", view.charge_view, name="charge"),
    
    # booking
    path("booking/", view.booking, name="booking"),
    
    # authentication & booking api
    path("api/v1/", include("api.urls", namespace="auth-api")),
]