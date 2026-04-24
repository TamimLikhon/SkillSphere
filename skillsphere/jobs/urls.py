from django.urls import path
from . import views

urlpatterns = [
    # Job URLs
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),

    # Application URLs
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('applications/', views.my_applications, name='my_applications'),

    # Invitation URLs
    path('invitations/', views.invitation_list, name='invitation_list'),
    path('invitations/send/', views.send_invitation, name='send_invitation'),
    path('invitations/<int:pk>/respond/', views.respond_invitation, name='respond_invitation'),

    # Offer URLs
    path('offers/', views.offer_list, name='offer_list'),
    path('offers/create/', views.create_offer, name='create_offer'),
    path('offers/<int:pk>/respond/', views.respond_offer, name='respond_offer'),
]