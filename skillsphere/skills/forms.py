from django import forms
from .models import Skill, CandidateSkill, Certificate, Assessment, JobSkillRequirement


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'category', 'description']


class CandidateSkillForm(forms.ModelForm):
    class Meta:
        model = CandidateSkill
        fields = ['candidate', 'skill', 'proficiency_level', 'years_of_experience', 'verified']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = [
            'candidate_skill',
            'title',
            'certificate_file',
            'issued_by',
            'issue_date',
            'expiry_date',
            'verification_status',
            'verified_by_admin'
        ]


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = [
            'candidate_skill',
            'test_type',
            'score',
            'passed',
            'attempt_time',
            'total_questions'
        ]


class JobSkillRequirementForm(forms.ModelForm):
    class Meta:
        model = JobSkillRequirement
        fields = ['job', 'skill', 'required_level', 'is_mandatory']