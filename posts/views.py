from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Categoria, Post


class AutorRequeridoMixin(UserPassesTestMixin):
    """Solo el autor del post puede editarlo o eliminarlo."""

    def test_func(self):
        return self.get_object().autor == self.request.user


class PostListView(ListView):
    model = Post
    paginate_by = 6
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.select_related("autor", "categoria")

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["categorias"] = Categoria.objects.all()
        return contexto


class PostsPorCategoriaView(PostListView):
    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs["slug"])
        return super().get_queryset().filter(categoria=self.categoria)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["categoria_actual"] = self.categoria
        return contexto


class PostSearchView(PostListView):
    template_name = "posts/buscar_posts.html"

    def get_queryset(self):
        self.query = self.request.GET.get("q", "").strip()
        if not self.query:
            return Post.objects.none()
        return (
            super()
            .get_queryset()
            .filter(Q(titulo__icontains=self.query) | Q(contenido__icontains=self.query))
        )

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["query"] = self.query
        return contexto


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    success_message = "Post publicado correctamente."

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, AutorRequeridoMixin, SuccessMessageMixin, UpdateView
):
    model = Post
    form_class = PostForm
    success_message = "Post actualizado correctamente."


class PostDeleteView(
    LoginRequiredMixin, AutorRequeridoMixin, SuccessMessageMixin, DeleteView
):
    model = Post
    context_object_name = "post"
    success_url = reverse_lazy("home")
    success_message = "Post eliminado."
