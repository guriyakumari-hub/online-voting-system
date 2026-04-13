from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('elections/', views.election_list, name='election_list'),
    path('elections/<int:pk>/', views.election_detail, name='election_detail'),
    path('elections/<int:pk>/vote/', views.cast_vote, name='cast_vote'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/elections/create/', views.election_create, name='election_create'),
    path('admin/elections/<int:pk>/edit/', views.election_edit, name='election_edit'),
    path('admin/elections/<int:pk>/delete/', views.election_delete, name='election_delete'),
    path('admin/candidates/', views.candidate_list, name='candidate_list'),
    path('admin/candidates/create/', views.candidate_create, name='candidate_create'),
    path('admin/candidates/<int:pk>/edit/', views.candidate_edit, name='candidate_edit'),
    path('admin/candidates/<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
]
