from django.urls import path
from .views import HomeView , detail , price_create ,prise_update ,login_ , logout_view
app_name = 'main'

urlpatterns  = [
    path('', HomeView.as_view() , name='home'),
    path('login/', login_ , name='login'),
    path('logout/', logout_view, name='logout'),
    path('detail/<int:pk>',detail,name='detail'),
    path('create/prise/<int:pk>',price_create,name='create'),
    path('update/price/<int:pk>',prise_update,name='create'),
]