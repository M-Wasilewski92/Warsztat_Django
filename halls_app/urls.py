from django.urls import path
from halls_app import views

urlpatterns = [
    path('new/', views.add_hall),
    path('<int:id>/', views.show_all),
    path('delete/<int:id>/', views.hall_remove)

]
