from django.urls import path
from . import views
from .views import patient_sign_up, doctor_sign_up
urlpatterns = [
    path('sign_up/patient/', patient_sign_up, name='patient_sign_up'),
    path('sign_up/doctor/', doctor_sign_up, name='doctor_sign_up'),
    path('sign_in',views.sign_in, name='sign_in'),
    path('',views.home, name='home'),
    path('logout/',views.logout,name='logout'),
]
