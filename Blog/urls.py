from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.Signup,name='signup'),
    path('login/',views.Login.as_view(),name = 'login'),
    path('',views.home, name = 'home'),
    path('Post-detail/<int:pk>/',views.Post_Detail, name='Post_Detail'),
    path('Search_Result/',views.Search_Result, name='Search_Result'),

    path('Category/<str:category>/',views.Category, name='category'),
]