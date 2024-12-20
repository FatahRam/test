from django.urls import path, include
from . import views

urlpatterns = [
    path('home',views.home,name="home"),
    path('',views.home2,name="home2"),
    path('home1',views.home1,name="home1"),
    path('register/',views.register, name="register"),
    path('connexion/',views.connexion,name="connexion"),
    path('show/<int:idl>/',views.show,name="show"),
    path('show1/<int:idl>/',views.show1,name="show1"),
    path('show2/<int:idl>/',views.show2,name="show2"),
    path('pre/<int:idl>/',views.pre,name="pre"),
    path('pre1/<int:idl>/',views.pre1,name="pre1"),
    path('his/<int:idl>/',views.his,name="his"),
    path('vis/<int:idl>/',views.vis,name="vis"),
    path('fus/',views.fus,name="fus"),
    path('deconnexion/',views.deconnexion,name="deconnexion"),
    
]