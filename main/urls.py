from django.urls import path
from .views import *
from .ajax import *
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
    path('tavar/',ProductView.as_view(),name='tavar'),
    path('order/',OrderView.as_view(),name='order'),
    path('save-data/', save_data, name='save_data'),
]