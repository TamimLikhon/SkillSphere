from django.contrib import admin
from .models import Interviewer, Shortlist, Interview
# Register your models here


from django.contrib import admin
from .models import Interviewer, Shortlist, Interview


admin.site.register(Interviewer)
admin.site.register(Shortlist)
admin.site.register(Interview)