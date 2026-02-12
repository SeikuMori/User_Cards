from django.urls import path
from . import views

# Пространство имён приложения — позволяет ссылаться на URL'ы как 'cards:person_list'
app_name = 'cards'

# Основной набор маршрутов для CRUD операций с моделью Person
urlpatterns = [
    # Список всех людей
    path('', views.PersonListView.as_view(), name='person_list'),
    # Создать нового человека
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    # Просмотреть детали человека по PK
    path('<int:pk>/', views.PersonDetailView.as_view(), name='person_detail'),
    # Редактировать существующую запись
    path('<int:pk>/edit/', views.PersonUpdateView.as_view(), name='person_edit'),
    # Удалить запись (DeleteView ожидает POST из шаблона)
    path('<int:pk>/delete/', views.PersonDeleteView.as_view(), name='person_delete'),
]