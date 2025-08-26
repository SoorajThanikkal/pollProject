from django.urls import path

from .import views
urlpatterns = [
    path("",views.MainPage,name="main"),
    path("register/", views.UserRegister, name="register"),
    path("login/", views.UserLogin, name="login"),
    path("logout/", views.UserLogout, name="logout"),
    
    path("adm/polls/", views.admin_poll_list, name="admin_poll_list"),
    path("adm/polls/<int:poll_id>/end/", views.end_poll, name="end_poll"),
    path("create/", views.create_poll, name="create_poll"),
    path("poll_list/", views.poll_list, name="poll_list"),
    path("<int:poll_id>/", views.poll_detail, name="poll_detail"),
    path("<int:poll_id>/results/", views.poll_results, name="poll_results"),
    path("delete_poll_votes/<int:poll_id>/", views.delete_poll_votes, name="delete_poll_votes"),
    
    #extra
    
    path("export_poll_excel/<int:poll_id>/", views.export_poll_excel, name="export_poll_excel"),
]
