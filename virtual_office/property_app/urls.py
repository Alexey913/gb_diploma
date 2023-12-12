from django.urls import path
from . import views
urlpatterns = [
               path('<int:user_id>/', views.get_properties, name='properties'),
               path('realty/<int:user_id>/', views.get_realty, name='realty'),
               path('transport/<int:user_id>/', views.get_transport, name='transport'),
               path('edit_realty/<int:user_id>/', views.edit_realty, name='edit_realty'),
               path('add_realty/<int:user_id>/', views.add_realty, name='add_realty'),
               path('show_realty/<int:user_id>/', views.show_realty_for_change, name='show_realty'),
               path('change_realty/<int:user_id>/<int:realty_id>/', views.change_realty, name='change_realty'),
               path('del_realty/<int:user_id>/<int:realty_id>/', views.del_realty, name='del_realty'),
               path('edit_transport/<int:user_id>/', views.edit_transport, name='edit_transport'),
               path('add_transport/<int:user_id>/', views.add_transport, name='add_transport'),
               path('show_transport/<int:user_id>/', views.show_transport_for_change, name='show_transport'),
               path('change_transport/<int:user_id>/<int:transport_id>/', views.change_transport, name='change_transport'),
               path('del_transport/<int:user_id>/<int:transport_id>/', views.del_transport, name='del_transport'),
               ]