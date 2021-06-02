from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('logout/', views.logoutUser, name="logout"),
    path('Tracker/',views.track,name="tracker"),
    path('deletePatient/<str:pid>/',views.deletePatient,name="delete"),
    path('Tracker/<str:pid>/',views.track,name="update"),
    path('addPatient/',views.track,name="add")
]