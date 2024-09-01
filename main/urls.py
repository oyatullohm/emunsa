from django.urls import path
from .views import *
from .ajax import *
app_name = 'main'

urlpatterns  = [
    path('', HomeVIew.as_view() , name='home'),
    path('cash/',CashView.as_view(), name='cash'),
    path('tavar/',ProductView.as_view(),name='tavar'),
    path('order/',OrderView.as_view(),name='order'),
    path('income/',IncomeView.as_view(),name='income'),
    path('emunsa/', EmunsaView.as_view() , name='emunsa'),
    path('client/', ClientViev.as_view() , name='client'),
    path('payment/',PaymentViev.as_view(), name='payment'),
    path('settings/',SettingsView.as_view(), name='settings'),
    path('login/', login_ , name='login'),
    path('logout/', logout_view, name='logout'),
    path('save-data/', save_data, name='save_data'),
    path('save-data/', save_data_income, name='save_data_income'),
    path('detail/<int:pk>',detail,name='detail'),
    path('update/price/<int:pk>',prise_update,name='create'),
    path('create/prise/<int:pk>',price_create,name='create'),
]