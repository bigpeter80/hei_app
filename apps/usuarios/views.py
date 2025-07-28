from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from .forms import LoginForm
from django.shortcuts import render, redirect
from apps.clientes.models import Cliente

class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    authentication_form = LoginForm

class UsuarioLogoutView(LogoutView):
    http_method_names = ['post']
    next_page = reverse_lazy('login')

@login_required
@never_cache
def dashboard_view(request):
    total_clientes = Cliente.objects.count()

    return render(request, 'usuarios/dashboard.html', {
        'usuario': request.user,
        'total_clientes': total_clientes,
    })


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')