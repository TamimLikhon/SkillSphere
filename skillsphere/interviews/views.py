from django.shortcuts import render, get_object_or_404, redirect
from .models import Interview, Shortlist, Interviewer


# Create your views here.
def interview_list(request):
    interviews = Interview.objects.all()
    return render(request, 'interviews/interview_list.html', {'interviews': interviews})


def interview_detail(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    return render(request, 'interviews/interview_detail.html', {'interview': interview})


def schedule_interview(request):
    if request.method == "POST":
        Interview.objects.create(
            candidate_id=request.POST['candidate'],
            interviewer_id=request.POST['interviewer'],
            job_id=request.POST['job'],
            interview_type=request.POST['type'],
            round_number=request.POST['round'],
            scheduled_date=request.POST['date'],
            scheduled_time=request.POST['time'],
        )
        return redirect('interview_list')

    return render(request, 'interviews/schedule_interview.html')


def submit_feedback(request, pk):
    interview = get_object_or_404(Interview, pk=pk)

    if request.method == "POST":
        interview.feedback = request.POST['feedback']
        interview.score = request.POST['score']
        interview.status = 'completed'
        interview.save()
        return redirect('interview_detail', pk=pk)

    return render(request, 'interviews/feedback_form.html', {'interview': interview})


def shortlist_list(request):
    data = Shortlist.objects.all()
    return render(request, 'interviews/shortlist.html', {'shortlists': data})


def add_shortlist(request):
    if request.method == "POST":
        Shortlist.objects.create(
            recruiter_id=request.POST['recruiter'],
            candidate_id=request.POST['candidate'],
            job_id=request.POST['job'],
            notes=request.POST.get('notes', '')
        )
        return redirect('shortlist_list')

    return render(request, 'interviews/shortlist.html')


def interviewer_list(request):
    interviewers = Interviewer.objects.all()
    return render(request, 'interviews/interviewer_list.html', {'interviewers': interviewers})
