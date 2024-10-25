from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from .models import User, Profile, Post, Comment, Payment
from .forms import RegisterForm, LoginForm, PostCreateForm, CommentForm, PaymentForm, ProfileUpdateForm


# Регистрация
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        return super().form_valid(form)

# Авторизация

class LoginView(CreateView):
    form_class = AuthenticationForm
    template_name = 'app/login.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, self.template_name, {'form': form})


# Главная страница с постами и профилями
class PostListView(ListView):
    model = Post
    template_name = 'app/base.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(user__profile__is_private=False) | Post.objects.filter(user=self.request.user)
        return Post.objects.filter(is_paid=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            followed_users = self.request.user.profile.following.all()
            not_followed_users = User.objects.exclude(id__in=followed_users.values_list('user__id', flat=True))

            # Пагинация профилей
            paginator = Paginator(not_followed_users, 3)  # 3 профиля на страницу
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['not_followed_profiles'] = page_obj
        return context

# Лайки для постов

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-detail', pk=pk)

# Просмотр детального поста
class PostDetailView(DetailView):
    model = Post
    template_name = 'app/detail.html'
    context_object_name = 'post'

# CRUD операции для постов
class PostCreateView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'app/create.html'
    success_url = reverse_lazy('home')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'app/update.html'
    success_url = reverse_lazy('home')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'app/delete.html'
    success_url = reverse_lazy('home')

# Комментарии к постам

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'app/add.html', {'form': form, 'post': post})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)

# Оплата постов и подписок

def pay_for_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.post = post
            payment.amount = post.price
            payment.save()
            return redirect('post-detail', pk=pk)
    else:
        form = PaymentForm()
    return render(request, 'app/pay.html', {'form': form, 'post': post})


def pay_for_subscription(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.subscription = True
            payment.amount = 10.00  # Стоимость подписки
            payment.save()
            return redirect('profile', pk=pk)
    else:
        form = PaymentForm()
    return render(request, 'app/pay_subscription.html', {'form': form, 'profile': profile})

def logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


class UserProfileView(DetailView):
    model = Profile
    template_name = 'app/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'app/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)