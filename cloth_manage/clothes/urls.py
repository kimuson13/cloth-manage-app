from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('top/<int:num>', views.top, name='top'),
    path('detail', views.top, name='detail'),
    path('post', views.post, name='post'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete'),
    path('search', views.search, name='search'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('logout', views.logout, {'template_name': 'index.html'}, name='logout'),
]