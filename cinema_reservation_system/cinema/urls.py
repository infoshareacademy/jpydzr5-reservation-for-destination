from . import views
from . import auth_views
from django.urls import path
from .views import user_panel_view

app_name = 'cinema'

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path("set_cinema", views.set_cinema, name="set_cinema"),
    path("ticket_types/", views.price_list, name="price_list"),
    path("repertoire/", views.repertoire, name="repertoire"),
    path("basket/", views.basket, name="basket"),
    path('select_movie/', views.select_movie, name='select_movie'),
    path('select_seance/<int:movie_id>/', views.select_seance, name='select_seance'),
    path('select_seats/<int:seance_id>/', views.select_seats, name='select_seats'),
    path('select_ticket_type/<int:reservation_id>/', views.select_ticket_type, name='select_ticket_type'),
    path('konto/', views.user_panel_view, name='user_panel'),
    path('konto/edytuj/', views.edit_user_panel_view, name='edit_user_panel'),
    path('qr_code/<int:reservation_id>/', views.qr_code_view, name='qr_code'),
    path('validate_ticket/<str:uuid>/', views.validate_ticket, name='validate_ticket'),
    path('validate_ticket/', views.validate_ticket, name='validate_ticket_home'),
    path('payment/', views.payment, name='pay_all'),
    path('tickets/', views.tickets, name='tickets'),
    path('payment/reservation/<int:reservation_id>/', views.payment, name='pay_one'),

]

