from django.db import models
from accounts.models import RecruiterProfile, CandidateProfile
from jobs.models import JobPost

# Create your models here.

class Interviewer(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class Shortlist(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    shortlisted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.candidate} - {self.job}"

class Interview(models.Model):
    TYPE = [('technical','Technical'),('hr','HR'),('final','Final')]
    STATUS = [('scheduled','Scheduled'),('completed','Completed'),('cancelled','Cancelled')]

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    interview_type = models.CharField(max_length=20, choices=TYPE)
    round_number = models.IntegerField()
    scheduled_date = models.DateField()
    scheduled_time = models.CharField(max_length=10)
    meeting_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default='scheduled')
    feedback = models.TextField(blank=True)
    score = models.FloatField(null=True, blank=True)
   
    class Meta:
        unique_together = ('candidate', 'job')
