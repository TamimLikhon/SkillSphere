from django.shortcuts import render, redirect, get_object_or_404
from .models import Interview, Interviewer, Shortlist
from .forms import InterviewForm, InterviewerForm, ShortlistForm

# Create your views here.

def interviewer_list(request):
    interviewers = Interviewer.objects.all()
    return render(request, 'interviewer/list.html', {'interviewers': interviewers})

def add_interviewer(request):
    form = InterviewerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('interviewer_list')
    return render(request, 'interviewer/form.html', {'form': form})

def shortlist_list(request):
    shortlists = Shortlist.objects.all()
    return render(request, 'shortlist/list.html', {'shortlists': shortlists})

def add_shortlist(request):
    form = ShortlistForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('shortlist_list')
    return render(request, 'shortlist/form.html', {'form': form})

def interview_list(request):
    interviews = Interview.objects.all()
    return render(request, 'interview/list.html', {'interviews': interviews})


def add_interview(request):
    form = InterviewForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('interview_list')
    return render(request, 'interview/form.html', {'form': form})

def interview_detail(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    return render(request, 'interview/detail.html', {'interview': interview})

def delete_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    interview.delete()
    return redirect('interview_list')
