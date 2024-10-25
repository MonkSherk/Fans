from django.urls import path

from . import views
from .views import (
    RegisterView, LoginView, PostListView, PostCreateView, PostDetailView,
    PostUpdateView, PostDeleteView, like_post, add_comment, delete_comment,
    pay_for_post, pay_for_subscription, UserProfileView, ProfileUpdateView
)

urlpatterns = [
    # Регистрация и авторизация
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    # Главная страница и посты
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),

    # Лайки и комментарии
    path('post/<int:pk>/like/', like_post, name='like-post'),
    path('post/<int:pk>/comment/', add_comment, name='add-comment'),
    path('comment/delete/<int:pk>/', delete_comment, name='delete-comment'),

    # Оплата
    path('post/<int:pk>/pay/', pay_for_post, name='pay-for-post'),
    path('profile/<int:pk>/pay_subscription/', pay_for_subscription, name='pay-for-subscription'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]
