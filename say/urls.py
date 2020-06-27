from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('order', views.order, name='order'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('handleSignup', views.handleSignup, name='handleSignup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login', views.login, name='login'),
    path('handleLogin', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='logout'),
    # path('series', views.series, name='series'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('subscriber_activate/<uidb64>/<token>', views.subscriber_activate, name='subscriber_activate'),
    # path('postComment', views.postComment, name='postComment'),  # this should be before slug url
    # path('series/<str:ser_slug>', views.series_list, name='series_list'),
    # path('<str:slug>', views.blogPost, name='blogPost'),
]