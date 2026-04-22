from django.shortcuts import render, redirect, get_object_or_404
from .models import Skill, CandidateSkill, Certificate, Assessment, JobSkillRequirement
from .forms import (
    SkillForm,
    CandidateSkillForm,
    CertificateForm,
    AssessmentForm,
    JobSkillRequirementForm
)

# ---------------- SKILL ----------------

def skill_list(request):
    skills = Skill.objects.all()
    return render(request, 'skills/skill_list.html', {'skills': skills})


def add_skill(request):
    form = SkillForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('skill_list')
    return render(request, 'skills/add_skill.html', {'form': form})


def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    form = SkillForm(request.POST or None, instance=skill)
    if form.is_valid():
        form.save()
        return redirect('skill_list')
    return render(request, 'skills/add_skill.html', {'form': form})


def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    return redirect('skill_list')


# ---------------- CANDIDATE SKILL ----------------

def candidate_skill_list(request):
    data = CandidateSkill.objects.all()
    return render(request, 'skills/my_skills.html', {'data': data})


def add_candidate_skill(request):
    form = CandidateSkillForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('my_skills')
    return render(request, 'skills/candidate_skill_form.html', {'form': form})


# ---------------- CERTIFICATE ----------------

def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'skills/certificate_list.html', {'certificates': certificates})


def add_certificate(request, pk):
    form = CertificateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        cert = form.save(commit=False)
        cert.candidate_skill_id = pk
        cert.save()
        return redirect('certificate_list')
    return render(request, 'skills/certificate_form.html', {'form': form})


def verify_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    certificate.verification_status = 'verified'
    certificate.verified_by_admin = True
    certificate.save()
    return redirect('certificate_list')


# ---------------- ASSESSMENT ----------------

def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'skills/assessment.html', {'assessments': assessments})


def add_assessment(request, pk):
    form = AssessmentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.candidate_skill_id = pk
        obj.save()
        return redirect('assessment')
    return render(request, 'skills/assessment_form.html', {'form': form})


# ---------------- JOB SKILL REQUIREMENT ----------------

def job_skill_requirement_list(request):
    data = JobSkillRequirement.objects.all()
    return render(request, 'skills/job_skill_requirement_list.html', {'data': data})


def add_job_skill_requirement(request):
    form = JobSkillRequirementForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('job_skill_requirement_list')
    return render(request, 'skills/job_skill_requirement_form.html', {'form': form})