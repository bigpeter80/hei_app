from django.urls import path
from .views import UsuarioLoginView, UsuarioLogoutView, dashboard_view, home_redirect

app_name = 'usuarios'

urlpatterns = [
    path('', home_redirect),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
