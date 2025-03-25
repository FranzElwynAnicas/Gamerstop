from django.urls import path
from . import views
from .views import games  

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('store/', views.store, name='store'),  
    path('freegames/', views.games, name='freegames'),
    path('store/<int:product_id>/', views.product_detail, name='product_detail'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('faq/', views.faq_view, name='faq'),
    path('news/', views.news_view, name='news'),
    path('chatbot/', views.chatbot_view, name='chatbot'),

]
