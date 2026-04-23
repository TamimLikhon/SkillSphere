from django.urls import path
from . import views

urlpatterns = [
    # Skill
    path('', views.skill_list, name='skill_list'),
    path('add/', views.add_skill, name='add_skill'),
    path('<int:pk>/edit/', views.edit_skill, name='edit_skill'),
    path('<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    # Candidate Skills
    path('my-skills/', views.candidate_skill_list, name='my_skills'),
    path('my-skills/add/', views.add_candidate_skill, name='add_candidate_skill'),

    # Certificate
    path('certificate/', views.certificate_list, name='certificate_list'),
    path('<int:pk>/certificate/add/', views.add_certificate, name='add_certificate'),
    path('verify/<int:pk>/', views.verify_certificate, name='verify_certificate'),

    # Assessment
    path('assessment/', views.assessment_list, name='assessment'),
    path('<int:pk>/assessment/add/', views.add_assessment, name='add_assessment'),

    # Job Skill Requirement
    path('job-skills/', views.job_skill_requirement_list, name='job_skill_requirement_list'),
    path('job-skills/add/', views.add_job_skill_requirement, name='add_job_skill_requirement'),
]