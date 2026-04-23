from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Skill, CandidateSkill, Certificate, Assessment, JobSkillRequirement

admin.site.register(Skill)
admin.site.register(CandidateSkill)
admin.site.register(Certificate)
admin.site.register(Assessment)
admin.site.register(JobSkillRequirement)