from django.urls import path
from halls_app import views

urlpatterns = [
    path('new/', views.add_hall),
    path('<int:hall_id>/', views.show_hall),
    path('delete/<int:hall_id>/', views.hall_remove),
    path('redirect/', views.show_hall),
    path('home/', views.show_all),
    path('modify/<int:hall_id>/', views.modify_hall),
    path('reserve/<int:hall_id>/', views.reserve_hall),

]
