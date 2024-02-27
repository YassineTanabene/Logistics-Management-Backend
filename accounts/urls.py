from django import views
from django.urls import path
from .views import camion_create, camion_delete, camion_retrieve, camion_update, register_user, user_login, user_logout,camion_list,camion_list_published

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create/', camion_create, name='create'),
    path('list/', camion_list, name='list'),
    path('update/<str:id>', camion_update, name='update'),
    path('retrieve/<str:id>', camion_retrieve, name='retrieve'),
    path('delete/<str:id>', camion_delete, name='delete'),


   
    

    
]
