from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import CandidateProfile, RecruiterProfile
from .models import JobPost, Application, HiringInvitation, JobOffer
from .forms import JobPostForm, ApplicationForm, HiringInvitationForm, JobOfferForm


# ─── Job List ─────────────────────────────────────────────────
def job_list(request):
    jobs = JobPost.objects.filter(status='open').order_by('-posted_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ─── Job Detail ───────────────────────────────────────────────
def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    already_applied = False
    if request.user.is_authenticated and request.user.role == 'candidate':
        already_applied = Application.objects.filter(
            candidate=request.user.candidateprofile, job=job
        ).exists()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
    })


# ─── Job Create (Recruiter only) ──────────────────────────────
@login_required
def job_create(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiterprofile
            job.save()
            messages.success(request, 'Job post created successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'New Job'})


# ─── Job Edit (Recruiter only) ────────────────────────────────
@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    if request.user.role != 'recruiter' or job.recruiter != request.user.recruiterprofile:
        return redirect('job_list')
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job'})


# ─── Apply to Job (Candidate only) ───────────────────────────
@login_required
def apply_job(request, pk):
    job = get_object_or_404(JobPost, pk=pk, status='open')
    if request.user.role != 'candidate':
        return redirect('job_list')
    if Application.objects.filter(candidate=request.user.candidateprofile, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = request.user.candidateprofile
            app.job = job
            app.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})


# ─── My Applications (Candidate only) ────────────────────────
@login_required
def my_applications(request):
    if request.user.role != 'candidate':
        return redirect('job_list')
    applications = Application.objects.filter(
        candidate=request.user.candidateprofile
    ).order_by('-applied_at')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


# ─── Invitation List ──────────────────────────────────────────
@login_required
def invitation_list(request):
    if request.user.role == 'recruiter':
        invitations = HiringInvitation.objects.filter(
            recruiter=request.user.recruiterprofile
        ).order_by('-created_at')
    else:
        invitations = HiringInvitation.objects.filter(
            candidate=request.user.candidateprofile
        ).order_by('-created_at')
    return render(request, 'jobs/invitation_list.html', {'invitations': invitations})


# ─── Send Invitation (Recruiter only) ────────────────────────
@login_required
def send_invitation(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')
    if request.method == 'POST':
        form = HiringInvitationForm(request.POST)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.recruiter = request.user.recruiterprofile
            inv.save()
            messages.success(request, 'Invitation sent successfully!')
            return redirect('invitation_list')
    else:
        form = HiringInvitationForm()
    return render(request, 'jobs/invitation_form.html', {'form': form})


# ─── Respond to Invitation (Candidate only) ──────────────────
@login_required
def respond_invitation(request, pk):
    inv = get_object_or_404(HiringInvitation, pk=pk, candidate=request.user.candidateprofile)
    action = request.POST.get('action')
    if action in ['accepted', 'rejected']:
        inv.status = action
        inv.response_date = timezone.now()
        inv.save()
    return redirect('invitation_list')


# ─── Offer List ───────────────────────────────────────────────
@login_required
def offer_list(request):
    if request.user.role == 'recruiter':
        offers = JobOffer.objects.filter(
            job__recruiter=request.user.recruiterprofile
        ).order_by('-created_at')
    else:
        offers = JobOffer.objects.filter(
            candidate=request.user.candidateprofile
        ).order_by('-created_at')
    return render(request, 'jobs/offer_list.html', {'offers': offers})


# ─── Create Offer (Recruiter only) ───────────────────────────
@login_required
def create_offer(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')
    if request.method == 'POST':
        form = JobOfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer sent successfully!')
            return redirect('offer_list')
    else:
        form = JobOfferForm()
    return render(request, 'jobs/offer_form.html', {'form': form})


# ─── Respond to Offer (Candidate only) ───────────────────────
@login_required
def respond_offer(request, pk):
    offer = get_object_or_404(JobOffer, pk=pk, candidate=request.user.candidateprofile)
    action = request.POST.get('action')
    if action in ['accepted', 'rejected']:
        offer.offer_status = action
        offer.save()
        messages.success(request, f'Offer {action} successfully!')
    return redirect('offer_list')