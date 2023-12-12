from django.urls import path
from . import views
urlpatterns = [
    path('<int:user_id>/', views.reminds, name='reminds'),
    path('add_remind/<int:user_id>/', views.add_remind, name='add_remind'),
    path('change_remind/<int:user_id>/<int:remind_id>/', views.change_remind, name='change_remind'),
    path('show_remind/<int:user_id>/<int:remind_id>/', views.show_remind, name='show_remind'),
    path('del_remind/<int:user_id>/<int:remind_id>/', views.del_remind, name='del_remind'),
    path('search/<int:user_id>/', views.search_reminds_by_title, name='search_by_title'),
               ]