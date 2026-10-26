from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import PerfilUsuarioForm, RegistroForm
from .models import PerfilUsuario


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "¡Cuenta creada! Ya iniciaste sesión.")
        return respuesta


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "usuarios/perfil.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["mis_posts"] = self.request.user.posts.select_related("categoria")
        return contexto


class PerfilEditarView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = PerfilUsuarioForm
    template_name = "usuarios/editar_perfil.html"
    success_url = reverse_lazy("perfil")
    success_message = "Perfil actualizado."

    def get_object(self, queryset=None):
        perfil, _ = PerfilUsuario.objects.get_or_create(user=self.request.user)
        return perfil
