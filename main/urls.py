from django.urls import path
from .views import *
app_name = 'main'

urlpatterns  = [
    path('', HomeVIew.as_view() , name='home'),
    path('emunsa/', EmunsaView.as_view() , name='emunsa'),
    path('client/', ClientViev.as_view() , name='client'),
    path('login/', login_ , name='login'),
    path('logout/', logout_view, name='logout'),
    path('detail/<int:pk>',detail,name='detail'),
    path('create/prise/<int:pk>',price_create,name='create'),
    path('update/price/<int:pk>',prise_update,name='create'),
]